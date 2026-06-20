"""Reconstroi os .msg traduzidos dentro da pasta do mod.

Reabre o .msg original (preservando cabecalhos, preambulo e mensagens nao
traduzidas) e substitui apenas o corpo das mensagens aprovadas. Os emuladores do
Persona Essentials (File Emulation Framework) compilam .msg -> .bmd em tempo de
execucao, entao nao precisamos reempacotar a CPK.
"""

from __future__ import annotations

from pathlib import Path

from .msg_format import parse_msg, serialize_msg
from .qa import tags_match
from .units import load_units, make_key


def build_mod(
    dump_dir: Path,
    translation_dir: Path,
    mod_dir: Path,
    only_status: tuple[str, ...] = ("reviewed", "final"),
) -> dict:
    dump_dir = Path(dump_dir)
    translation_dir = Path(translation_dir)
    mod_dir = Path(mod_dir)
    stats = {"files": 0, "messages": 0, "skipped": 0}

    for json_path in sorted(translation_dir.rglob("*.json")):
        rel = json_path.relative_to(translation_dir).as_posix()
        if rel.endswith(".json"):
            rel = rel[:-5]
        src_msg = dump_dir / rel
        if not src_msg.exists():
            stats["skipped"] += 1
            continue

        by_key = {u.key: u for u in load_units(json_path)}
        mf = parse_msg(src_msg.read_text(encoding="utf-8"))
        changed = False
        for i, msg in enumerate(mf.messages):
            u = by_key.get(make_key(rel, msg, i))
            if not u or u.status not in only_status or not u.target.strip():
                continue
            if not tags_match(u.source, u.target):
                stats["skipped"] += 1
                continue
            msg.set_body(u.target)
            changed = True
            stats["messages"] += 1

        if changed:
            # Espelha o caminho do arquivo dentro da CPK (veja mod/README.md).
            out = mod_dir / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(serialize_msg(mf), encoding="utf-8")
            stats["files"] += 1

    return stats
