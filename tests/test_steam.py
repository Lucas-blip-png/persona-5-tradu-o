from p5r_ptbr_installer import steam


def test_parse_vdf_paths_desescapa_barras():
    vdf = '''"libraryfolders"
{
    "0" { "path" "C:\\\\Program Files (x86)\\\\Steam" }
    "1" { "path" "D:\\\\SteamLibrary" }
}'''
    paths = steam.parse_vdf_paths(vdf)
    assert paths == ["C:\\Program Files (x86)\\Steam", "D:\\SteamLibrary"]


def test_parse_acf_installdir():
    acf = '"AppState"\n{\n  "appid" "1687950"\n  "installdir" "P5R"\n}'
    assert steam.parse_acf_installdir(acf) == "P5R"
    assert steam.parse_acf_installdir("{}") is None


def test_find_game_via_steam(tmp_path):
    # Biblioteca secundaria com o jogo instalado.
    lib = tmp_path / "Lib2"
    common = lib / "steamapps" / "common" / "P5R"
    common.mkdir(parents=True)
    (common / "P5R.exe").write_text("", encoding="utf-8")
    (lib / "steamapps" / f"appmanifest_{steam.P5R_STEAM_APPID}.acf").write_text(
        '"AppState"\n{\n  "appid" "1687950"\n  "installdir" "P5R"\n}', encoding="utf-8"
    )

    # Raiz Steam aponta para a biblioteca secundaria via libraryfolders.vdf.
    root = tmp_path / "Steam"
    (root / "steamapps").mkdir(parents=True)
    lib_escaped = str(lib).replace("\\", "\\\\")
    (root / "steamapps" / "libraryfolders.vdf").write_text(
        f'"libraryfolders" {{ "0" {{ "path" "{lib_escaped}" }} }}', encoding="utf-8"
    )

    found = steam.find_game_via_steam(steam_roots=[root])
    assert found == common
    assert steam.looks_like_game_dir(found)


def test_find_game_via_steam_nao_encontra(tmp_path):
    assert steam.find_game_via_steam(steam_roots=[tmp_path / "inexistente"]) is None
