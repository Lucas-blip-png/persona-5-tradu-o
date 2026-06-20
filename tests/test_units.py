from pathlib import Path

from p5r_ptbr.msg_format import parse_msg
from p5r_ptbr.units import (
    load_units,
    merge_units,
    save_units,
    units_from_file,
)

FIXTURE = Path(__file__).parent / "fixtures" / "exemplo.msg"


def _fresh():
    mf = parse_msg(FIXTURE.read_text(encoding="utf-8"))
    return units_from_file("exemplo.msg", mf)


def test_geracao_de_unidades():
    units = _fresh()
    assert len(units) == 3
    assert units[0].key == "exemplo.msg::msg:test_hello#0"
    assert units[0].speaker == "Hero"
    assert units[0].status == "untranslated"
    # Contexto deve referenciar a mensagem vizinha.
    assert "Guide" in units[0].context


def test_io_json_roundtrip(tmp_path):
    units = _fresh()
    out = tmp_path / "exemplo.msg.json"
    save_units(out, "exemplo.msg", units)
    carregadas = load_units(out)
    assert [u.key for u in carregadas] == [u.key for u in units]


def test_merge_preserva_traducao_quando_fonte_igual():
    existing = _fresh()
    existing[0].target = "Ola, viajante.[e]"
    existing[0].status = "reviewed"
    merged = merge_units(existing, _fresh())
    assert merged[0].target == "Ola, viajante.[e]"
    assert merged[0].status == "reviewed"


def test_merge_reseta_quando_fonte_muda():
    existing = _fresh()
    existing[0].target = "Ola, viajante.[e]"
    existing[0].status = "final"
    existing[0].source = "Texto antigo e diferente.[e]"
    merged = merge_units(existing, _fresh())
    assert merged[0].status == "untranslated"
    assert merged[0].target == ""
    assert "traducao anterior" in merged[0].notes
