"""Unidade de traducao + I/O JSON + merge incremental.

Cada mensagem traduzivel vira uma ``TranslationUnit`` com chave estavel, para que
reextrair os arquivos do jogo nao apague o trabalho ja feito.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .msg_format import Message, MessageFile, visible_text

STATUSES = ("untranslated", "draft", "reviewed", "final")
_FIELDS = {
    "key", "file", "kind", "name", "speaker",
    "source", "target", "status", "context", "notes",
}


@dataclass
class TranslationUnit:
    key: str
    file: str
    kind: str
    name: str
    speaker: str | None
    source: str
    target: str = ""
    status: str = "untranslated"
    context: str = ""
    notes: str = ""


def make_key(rel_file: str, msg: Message, index: int) -> str:
    """Chave estavel: arquivo + tipo + nome + indice (desambigua nomes repetidos)."""
    return f"{rel_file}::{msg.kind}:{msg.name}#{index}"


def _summary(msg: Message, limit: int = 120) -> str:
    text = visible_text(msg.body).replace("\n", " ").strip()
    if len(text) > limit:
        text = text[:limit] + "..."
    who = msg.speaker or msg.name
    return f"{who}: {text}" if text else ""


def units_from_file(rel_file: str, mf: MessageFile) -> list[TranslationUnit]:
    """Gera as unidades de uma mensagem, com contexto das linhas vizinhas."""
    units: list[TranslationUnit] = []
    msgs = mf.messages
    for i, msg in enumerate(msgs):
        source = msg.body
        if not source.strip():
            continue  # sem texto para traduzir
        prev_ctx = _summary(msgs[i - 1]) if i > 0 else ""
        next_ctx = _summary(msgs[i + 1]) if i + 1 < len(msgs) else ""
        context = "\n".join(c for c in (prev_ctx, next_ctx) if c)
        units.append(
            TranslationUnit(
                key=make_key(rel_file, msg, i),
                file=rel_file,
                kind=msg.kind,
                name=msg.name,
                speaker=msg.speaker,
                source=source,
                context=context,
            )
        )
    return units


def save_units(path: Path, rel_file: str, units: list[TranslationUnit]) -> None:
    payload = {"version": 1, "file": rel_file, "units": [asdict(u) for u in units]}
    Path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def load_units(path: Path) -> list[TranslationUnit]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = data["units"] if isinstance(data, dict) else data
    return [TranslationUnit(**{k: v for k, v in row.items() if k in _FIELDS}) for row in rows]


def merge_units(
    existing: list[TranslationUnit], fresh: list[TranslationUnit]
) -> list[TranslationUnit]:
    """Mescla mantendo traducao previa quando a fonte nao mudou.

    - fonte igual: carrega target/status/notes antigos (contexto vem do fresh).
    - fonte mudou: usa o fresh (untranslated) e guarda a traducao antiga em notes.
    - chave nova: adiciona.
    Chaves removidas do jogo deixam de aparecer.
    """
    old = {u.key: u for u in existing}
    result: list[TranslationUnit] = []
    for u in fresh:
        prev = old.get(u.key)
        if prev is None:
            result.append(u)
        elif prev.source == u.source:
            u.target = prev.target
            u.status = prev.status
            u.notes = prev.notes
            result.append(u)
        else:
            if prev.target.strip():
                note = f"fonte alterada; traducao anterior: {prev.target!r}"
                u.notes = f"{u.notes} | {note}".strip(" |") if u.notes else note
            result.append(u)
    return result
