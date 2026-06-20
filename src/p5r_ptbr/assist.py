"""Assistente de localizacao via IA (Claude) — gera RASCUNHOS, nunca o final.

Este passo e opcional e desligado por padrao. Quando ativado, monta um prompt rico
(trecho original + falante + contexto da cena + glossario + guia de estilo + voz do
personagem) e pede ao Claude um rascunho de qualidade em PT-BR. Toda saida e marcada
como ``draft`` e DEVE passar por revisao humana antes de virar ``reviewed``/``final``.

Nao e traducao generica de maquina: o objetivo e fidelidade ao sentido com adaptacao
natural de girias e referencias, respeitando a voz de cada personagem.

Requer: ``pip install -e ".[assist]"`` e a variavel de ambiente ``ANTHROPIC_API_KEY``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .glossary import Glossary
from .units import TranslationUnit

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = """\
Voce e um localizador profissional de games, traduzindo Persona 5 Royal do ingles
para o portugues brasileiro (PT-BR). Prioridades, em ordem:

1. Fidelidade ao sentido e a intencao do original (NAO traduza palavra por palavra).
2. Naturalidade: o dialogo deve soar como um brasileiro falaria de verdade.
3. Adapte girias, trocadilhos e referencias culturais para equivalentes em PT-BR.
4. Respeite a voz do personagem (registro, formalidade, bordoes) informada no contexto.
5. PRESERVE EXATAMENTE todas as tags de controle entre colchetes (ex.: [e], [n],
   [f 2 1]) — mesma quantidade, mesmo conteudo, nas posicoes equivalentes.
6. Respeite o glossario fornecido (use sempre o termo PT-BR indicado).

Responda APENAS com o texto traduzido (com as tags preservadas), sem comentarios,
sem aspas e sem explicacoes.\
"""


@dataclass
class AssistConfig:
    style_guide: str = ""
    character_voices: str = ""
    glossary: Glossary | None = None
    model: str = MODEL


def available() -> bool:
    """True se a SDK do Anthropic estiver instalada e a chave estiver no ambiente."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return False
    try:
        import anthropic  # noqa: F401
    except ImportError:
        return False
    return True


def _build_user_prompt(unit: TranslationUnit, cfg: AssistConfig) -> str:
    parts: list[str] = []
    if cfg.style_guide:
        parts.append(f"## Guia de estilo\n{cfg.style_guide}")
    if cfg.character_voices:
        parts.append(f"## Vozes dos personagens\n{cfg.character_voices}")
    if cfg.glossary:
        relevant = cfg.glossary.relevant(unit.source)
        if relevant:
            linhas = "\n".join(f"- {e.en} -> {e.pt_br}" for e in relevant)
            parts.append(f"## Glossario relevante\n{linhas}")
    if unit.speaker:
        parts.append(f"## Falante\n{unit.speaker}")
    if unit.context:
        parts.append(f"## Contexto da cena (linhas vizinhas)\n{unit.context}")
    parts.append(f"## Texto original (traduza para PT-BR, preservando as tags)\n{unit.source}")
    return "\n\n".join(parts)


def draft_unit(unit: TranslationUnit, cfg: AssistConfig) -> str:
    """Retorna um rascunho PT-BR para a unidade (nao altera a unidade)."""
    import anthropic

    client = anthropic.Anthropic()
    user_prompt = _build_user_prompt(unit, cfg)
    # Streaming + adaptive thinking: rascunho de qualidade com baixo risco de timeout.
    with client.messages.stream(
        model=cfg.model,
        max_tokens=2000,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        message = stream.get_final_message()

    return "".join(b.text for b in message.content if b.type == "text").strip()


def draft_units(
    units: list[TranslationUnit], cfg: AssistConfig, limit: int | None = None
) -> int:
    """Preenche rascunhos para unidades 'untranslated'. Marca status='draft'."""
    drafted = 0
    for u in units:
        if limit is not None and drafted >= limit:
            break
        if u.status != "untranslated" or u.target.strip():
            continue
        u.target = draft_unit(u, cfg)
        u.status = "draft"
        u.notes = (f"{u.notes} | auto: rascunho de IA (revisar)".strip(" |")
                   if u.notes else "auto: rascunho de IA (revisar)")
        drafted += 1
    return drafted


def load_config(repo_root: Path, glossary: Glossary | None) -> AssistConfig:
    """Carrega guia de estilo e vozes de personagem do diretorio glossary/."""
    root = Path(repo_root)
    style = root / "glossary" / "guia-de-estilo.md"
    voices = root / "glossary" / "vozes-personagens.md"
    return AssistConfig(
        style_guide=style.read_text(encoding="utf-8") if style.exists() else "",
        character_voices=voices.read_text(encoding="utf-8") if voices.exists() else "",
        glossary=glossary,
    )
