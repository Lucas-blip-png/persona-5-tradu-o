"""Checagens de qualidade (QA) antes de gerar o mod.

Verifica: tags de controle preservadas, alvo vazio em unidades aprovadas, limite
de caracteres da UI, aderencia ao glossario e quanto ainda falta traduzir.
O build so aceita unidades 'reviewed'/'final' que passem na checagem de tags.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

from .glossary import Glossary
from .msg_format import extract_tags, visible_text
from .units import TranslationUnit


@dataclass
class QAReport:
    total: int = 0
    untranslated: int = 0
    tag_mismatches: list[str] = field(default_factory=list)
    missing_target: list[str] = field(default_factory=list)
    too_long: list[tuple[str, int]] = field(default_factory=list)
    glossary: list[tuple[str, str]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not (self.tag_mismatches or self.missing_target)


def tags_match(source: str, target: str) -> bool:
    """As tags de controle sao identicas (mesmo conjunto e contagem)."""
    return Counter(extract_tags(source)) == Counter(extract_tags(target))


def run_qa(
    units: list[TranslationUnit],
    glossary: Glossary | None = None,
    max_visible_len: int | None = None,
) -> QAReport:
    rep = QAReport(total=len(units))
    for u in units:
        if u.status == "untranslated":
            rep.untranslated += 1
            continue
        if not u.target.strip():
            rep.missing_target.append(u.key)
            continue
        if not tags_match(u.source, u.target):
            rep.tag_mismatches.append(u.key)
        if max_visible_len:
            for line in visible_text(u.target).split("\n"):
                if len(line) > max_visible_len:
                    rep.too_long.append((u.key, len(line)))
                    break
        if glossary:
            for v in glossary.violations(u):
                rep.glossary.append((u.key, v))
    return rep


def buildable(units: list[TranslationUnit]) -> list[TranslationUnit]:
    """Unidades aptas a entrar no mod: aprovadas, com alvo e tags intactas."""
    return [
        u
        for u in units
        if u.status in ("reviewed", "final") and u.target.strip() and tags_match(u.source, u.target)
    ]
