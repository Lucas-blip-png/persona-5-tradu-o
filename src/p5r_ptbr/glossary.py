"""Glossario de decisoes de traducao (consistencia de termos).

O CSV em ``glossary/glossario.pt-br.csv`` lista termo EN -> PT-BR escolhido. Aqui
carregamos esse glossario para (1) alimentar o assistente de IA com os termos
relevantes a cada trecho e (2) validar (QA) se a traducao respeita as escolhas.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

from .units import TranslationUnit


@dataclass
class GlossaryEntry:
    en: str
    pt_br: str
    categoria: str = ""
    nota: str = ""


class Glossary:
    def __init__(self, entries: list[GlossaryEntry]) -> None:
        self.entries = entries

    @classmethod
    def load(cls, path: Path) -> Glossary:
        entries: list[GlossaryEntry] = []
        with open(path, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                en = (row.get("en") or "").strip()
                if not en:
                    continue
                entries.append(
                    GlossaryEntry(
                        en=en,
                        pt_br=(row.get("pt_br") or "").strip(),
                        categoria=(row.get("categoria") or "").strip(),
                        nota=(row.get("nota") or "").strip(),
                    )
                )
        return cls(entries)

    def relevant(self, source: str) -> list[GlossaryEntry]:
        """Entradas cujo termo EN aparece na fonte (para guiar a traducao)."""
        low = source.lower()
        return [e for e in self.entries if e.en.lower() in low]

    def violations(self, unit: TranslationUnit) -> list[str]:
        """Avisos quando a fonte usa um termo do glossario e o alvo nao usa o PT-BR."""
        msgs: list[str] = []
        if not unit.target.strip():
            return msgs
        low_src = unit.source.lower()
        low_tgt = unit.target.lower()
        for e in self.entries:
            if not e.pt_br:
                continue
            if re.search(rf"\b{re.escape(e.en.lower())}\b", low_src) and e.pt_br.lower() not in low_tgt:
                msgs.append(f"termo '{e.en}' deveria aparecer como '{e.pt_br}'")
        return msgs
