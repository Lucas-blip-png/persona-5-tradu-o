from p5r_ptbr.glossary import Glossary
from p5r_ptbr.units import TranslationUnit

CSV = "en,pt_br,categoria,nota\nConfidant,Confidente,sistema,\nPalace,Palacio,local,\n"


def _glossary(tmp_path):
    path = tmp_path / "g.csv"
    path.write_text(CSV, encoding="utf-8")
    return Glossary.load(path)


def _unit(source, target):
    return TranslationUnit(
        key="k", file="f", kind="msg", name="n", speaker=None, source=source, target=target
    )


def test_relevant(tmp_path):
    g = _glossary(tmp_path)
    rel = g.relevant("Visit the Palace today")
    assert [e.en for e in rel] == ["Palace"]


def test_violation_detectada(tmp_path):
    g = _glossary(tmp_path)
    u = _unit("The Confidant arrived.", "O aliado chegou.")
    assert g.violations(u)  # nao usou "Confidente"


def test_sem_violacao_quando_termo_correto(tmp_path):
    g = _glossary(tmp_path)
    u = _unit("The Confidant arrived.", "O Confidente chegou.")
    assert g.violations(u) == []
