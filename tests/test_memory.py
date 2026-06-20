from p5r_ptbr.memory import TranslationMemory, apply_memory
from p5r_ptbr.units import TranslationUnit


def _unit(source, target="", status="untranslated"):
    return TranslationUnit(
        key=source, file="f", kind="msg", name="n", speaker=None,
        source=source, target=target, status=status,
    )


def test_build_from_units_so_aprovadas():
    units = [
        _unit("Hello[e]", "Ola[e]", "reviewed"),
        _unit("Bye[e]", "Tchau[e]", "draft"),  # rascunho nao entra na TM
    ]
    tm = TranslationMemory.build_from_units(units)
    assert tm.lookup("Hello[e]") == "Ola[e]"
    assert tm.lookup("Bye[e]") is None


def test_apply_memory_preenche_match_exato():
    tm = TranslationMemory()
    tm.add("Hello[e]", "Ola[e]")
    pendentes = [_unit("Hello[e]"), _unit("Other[e]")]
    filled = apply_memory(pendentes, tm)
    assert filled == 1
    assert pendentes[0].target == "Ola[e]"
    assert pendentes[0].status == "draft"
    assert pendentes[1].target == ""


def test_fuzzy():
    tm = TranslationMemory()
    tm.add("Hello there[e]", "Ola[e]")
    assert tm.fuzzy("Hello there![e]", threshold=0.8) is not None
    assert tm.fuzzy("Totalmente diferente", threshold=0.8) is None
