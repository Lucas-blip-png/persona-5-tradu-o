"""Memoria de traducao (TM): reaproveita traducoes ja aprovadas.

Mantem consistencia e reduz retrabalho preenchendo automaticamente unidades cuja
fonte e identica a uma traducao ja revisada/finalizada.
"""

from __future__ import annotations

import difflib
from collections.abc import Iterable

from .units import TranslationUnit


class TranslationMemory:
    def __init__(self) -> None:
        self._exact: dict[str, str] = {}

    def add(self, source: str, target: str) -> None:
        if source and target:
            self._exact.setdefault(source, target)

    def lookup(self, source: str) -> str | None:
        return self._exact.get(source)

    def fuzzy(self, source: str, threshold: float = 0.9) -> tuple[str, float] | None:
        best: str | None = None
        best_ratio = 0.0
        for cand_src, cand_tgt in self._exact.items():
            ratio = difflib.SequenceMatcher(None, source, cand_src).ratio()
            if ratio > best_ratio:
                best_ratio, best = ratio, cand_tgt
        if best is not None and best_ratio >= threshold:
            return best, best_ratio
        return None

    @classmethod
    def build_from_units(cls, units: Iterable[TranslationUnit]) -> TranslationMemory:
        tm = cls()
        for u in units:
            if u.status in ("reviewed", "final") and u.target.strip():
                tm.add(u.source, u.target)
        return tm


def _append_note(notes: str, extra: str) -> str:
    return f"{notes} | {extra}".strip(" |") if notes else extra


def apply_memory(units: list[TranslationUnit], tm: TranslationMemory) -> int:
    """Preenche unidades 'untranslated' com matches exatos da TM (status -> draft)."""
    filled = 0
    for u in units:
        if u.status == "untranslated" and not u.target:
            hit = tm.lookup(u.source)
            if hit:
                u.target = hit
                u.status = "draft"
                u.notes = _append_note(u.notes, "auto: memoria de traducao (match exato)")
                filled += 1
    return filled
