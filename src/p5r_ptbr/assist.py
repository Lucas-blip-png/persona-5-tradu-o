"""Assistente de localizacao via IA (opcional) — gera RASCUNHOS, nunca o final.

Opcional e desligado por padrao. Quando configurado, monta um prompt rico
(trecho original + falante + contexto da cena + glossario + guia de estilo + voz
do personagem) e pede a um provedor de IA um rascunho de qualidade em PT-BR. Toda
saida e marcada como ``draft`` e DEVE passar por revisao humana antes de virar
``reviewed``/``final``.

Nao e traducao generica de maquina: o objetivo e fidelidade ao sentido com
adaptacao natural de girias e referencias, respeitando a voz de cada personagem.

Provedor a sua escolha (qualquer API compativel com "chat completions" no estilo
OpenAI). Configuracao por variaveis de ambiente:
  - ``P5R_AI_API_URL``  (ex.: ``https://SEU-PROVEDOR/v1/chat/completions``)
  - ``P5R_AI_API_KEY``
  - ``P5R_AI_MODEL``
"""

from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .glossary import Glossary
from .units import TranslationUnit

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
    api_url: str = ""
    api_key: str = ""
    model: str = ""


def available() -> bool:
    """True se as variaveis de ambiente do provedor de IA estiverem definidas."""
    return bool(
        os.environ.get("P5R_AI_API_URL")
        and os.environ.get("P5R_AI_API_KEY")
        and os.environ.get("P5R_AI_MODEL")
    )


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
    payload = {
        "model": cfg.model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": _build_user_prompt(unit, cfg)},
        ],
        "temperature": 0.3,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        cfg.api_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {cfg.api_key}",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        out = json.load(resp)
    return out["choices"][0]["message"]["content"].strip()


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
        u.notes = (
            f"{u.notes} | auto: rascunho de IA (revisar)".strip(" |")
            if u.notes
            else "auto: rascunho de IA (revisar)"
        )
        drafted += 1
    return drafted


def load_config(repo_root: Path, glossary: Glossary | None) -> AssistConfig:
    """Carrega guia de estilo e vozes de personagem + config do provedor (env)."""
    root = Path(repo_root)
    style = root / "glossary" / "guia-de-estilo.md"
    voices = root / "glossary" / "vozes-personagens.md"
    return AssistConfig(
        style_guide=style.read_text(encoding="utf-8") if style.exists() else "",
        character_voices=voices.read_text(encoding="utf-8") if voices.exists() else "",
        glossary=glossary,
        api_url=os.environ.get("P5R_AI_API_URL", ""),
        api_key=os.environ.get("P5R_AI_API_KEY", ""),
        model=os.environ.get("P5R_AI_MODEL", ""),
    )
