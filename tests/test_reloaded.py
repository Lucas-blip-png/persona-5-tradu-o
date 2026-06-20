import json

from p5r_ptbr_installer import reloaded


def test_merge_enabled_mods_adiciona_sem_duplicar():
    cfg = {"EnabledMods": ["existente"]}
    out = reloaded.merge_enabled_mods(cfg, ["existente", "p5r.ptbr"])
    assert out["EnabledMods"] == ["existente", "p5r.ptbr"]


def test_install_mod_files_copia_arvore(tmp_path):
    src = tmp_path / "modsrc"
    (src / "P5R").mkdir(parents=True)
    (src / "ModConfig.json").write_text("{}", encoding="utf-8")
    (src / "P5R" / "a.msg").write_text("x", encoding="utf-8")

    mods_dir = tmp_path / "Mods"
    dest = reloaded.install_mod_files(mods_dir, src, "p5r.ptbr")
    assert (dest / "ModConfig.json").exists()
    assert (dest / "P5R" / "a.msg").exists()


def test_enable_mod_in_app_configs(tmp_path):
    app_dir = tmp_path / "Apps" / "abc"
    app_dir.mkdir(parents=True)
    cfg = app_dir / "AppConfig.json"
    cfg.write_text(
        json.dumps({"AppId": "p5r.exe", "AppLocation": "D:\\Games\\P5R\\P5R.exe", "EnabledMods": []}),
        encoding="utf-8",
    )
    changed = reloaded.enable_mod_in_app_configs(tmp_path, ["p5r.ptbr"])
    assert changed == [cfg]
    assert "p5r.ptbr" in json.loads(cfg.read_text(encoding="utf-8"))["EnabledMods"]


def test_mod_dependencies_le_modconfig(tmp_path):
    src = tmp_path / "mod"
    src.mkdir()
    (src / "ModConfig.json").write_text(
        json.dumps({"ModDependencies": ["p5rpc.modloader", "reloaded.universal.fileemulationframework"]}),
        encoding="utf-8",
    )
    assert reloaded.mod_dependencies(src) == [
        "p5rpc.modloader",
        "reloaded.universal.fileemulationframework",
    ]
