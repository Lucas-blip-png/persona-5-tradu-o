"""Constroi/atualiza as unidades de traducao (JSON) a partir dos .msg extraidos.

Mescla de forma incremental (preserva trabalho ja feito) e aplica a memoria de
traducao (TM) construida a partir das traducoes ja aprovadas.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from .memory import TranslationMemory, apply_memory
from .msg_format import parse_msg
from .units import load_units, merge_units, save_units, units_from_file


def iter_msg_files(dump_dir: Path) -> Iterable[Path]:
    return sorted(Path(dump_dir).rglob("*.msg"))


def _json_path(translation_dir: Path, rel_file: str) -> Path:
    return Path(translation_dir) / (rel_file + ".json")


def _global_memory(translation_dir: Path) -> TranslationMemory:
    tm = TranslationMemory()
    for jp in Path(translation_dir).rglob("*.json"):
        for u in load_units(jp):
            if u.status in ("reviewed", "final") and u.target.strip():
                tm.add(u.source, u.target)
    return tm


def build_units(dump_dir: Path, translation_dir: Path, use_memory: bool = True) -> dict:
    dump_dir = Path(dump_dir)
    translation_dir = Path(translation_dir)
    tm = _global_memory(translation_dir) if use_memory else TranslationMemory()
    stats = {"files": 0, "units": 0, "reused": 0}

    for msg_path in iter_msg_files(dump_dir):
        rel = msg_path.relative_to(dump_dir).as_posix()
        mf = parse_msg(msg_path.read_text(encoding="utf-8"))
        fresh = units_from_file(rel, mf)

        out = _json_path(translation_dir, rel)
        merged = merge_units(load_units(out), fresh) if out.exists() else fresh
        if use_memory:
            stats["reused"] += apply_memory(merged, tm)

        out.parent.mkdir(parents=True, exist_ok=True)
        save_units(out, rel, merged)
        stats["files"] += 1
        stats["units"] += len(merged)

    return stats
