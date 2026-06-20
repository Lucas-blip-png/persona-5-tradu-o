from p5r_ptbr.qa import buildable, run_qa, tags_match
from p5r_ptbr.units import TranslationUnit


def _unit(source, target, status="reviewed", key="k"):
    return TranslationUnit(
        key=key, file="f", kind="msg", name="n", speaker=None,
        source=source, target=target, status=status,
    )


def test_tags_match():
    assert tags_match("Hi[f 2 1]there[e]", "Oi[f 2 1]ali[e]")
    assert not tags_match("Hi[e]", "Oi")


def test_run_qa_detecta_tags_divergentes():
    units = [_unit("Hi[e]", "Oi", key="bad")]
    rep = run_qa(units)
    assert rep.tag_mismatches == ["bad"]
    assert not rep.ok


def test_run_qa_conta_untranslated():
    units = [_unit("Hi[e]", "", status="untranslated")]
    rep = run_qa(units)
    assert rep.untranslated == 1
    assert rep.ok  # untranslated nao quebra o QA


def test_buildable_filtra_aprovadas_e_validas():
    units = [
        _unit("Hi[e]", "Oi[e]", status="final", key="ok"),
        _unit("Hi[e]", "Oi", status="reviewed", key="tags"),       # tag faltando
        _unit("Hi[e]", "Oi[e]", status="draft", key="rascunho"),   # nao aprovada
    ]
    keys = [u.key for u in buildable(units)]
    assert keys == ["ok"]
