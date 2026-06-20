from pathlib import Path

from p5r_ptbr.msg_format import (
    extract_tags,
    parse_msg,
    serialize_msg,
    visible_text,
)

FIXTURE = Path(__file__).parent / "fixtures" / "exemplo.msg"


def test_round_trip_exato():
    text = FIXTURE.read_text(encoding="utf-8")
    assert serialize_msg(parse_msg(text)) == text


def test_round_trip_casos_de_borda():
    for text in ("", "abc", "[msg a]\n[msg b]\n", "preambulo\n[msg a]\nx[e]"):
        assert serialize_msg(parse_msg(text)) == text


def test_parse_metadados():
    mf = parse_msg(FIXTURE.read_text(encoding="utf-8"))
    assert [m.name for m in mf.messages] == ["test_hello", "test_warn", "test_choice"]
    assert mf.messages[0].kind == "msg"
    assert mf.messages[0].speaker == "Hero"
    assert mf.messages[2].kind == "sel"
    assert mf.messages[2].speaker is None


def test_extract_tags_e_texto_visivel():
    mf = parse_msg(FIXTURE.read_text(encoding="utf-8"))
    warn = mf.messages[1]
    assert extract_tags(warn.body) == ["[f 2 1]", "[f 2 2]", "[n]", "[e]"]
    assert "[f 2 1]" not in visible_text(warn.body)
    assert "trap" in visible_text(warn.body)


def test_set_body_preserva_estrutura():
    mf = parse_msg(FIXTURE.read_text(encoding="utf-8"))
    mf.messages[0].set_body("Ola, viajante.[e]")
    assert "Ola, viajante.[e]" in serialize_msg(mf)
    assert "[msg test_hello [Hero]]" in serialize_msg(mf)
