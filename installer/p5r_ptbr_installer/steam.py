"""Deteccao do Persona 5 Royal instalado via Steam.

Funcoes puras e testaveis: parse do ``libraryfolders.vdf`` e do ``appmanifest``,
varredura das bibliotecas Steam e localizacao da pasta do jogo.
"""

from __future__ import annotations

import re
from pathlib import Path

# AppID do Persona 5 Royal na Steam e nome do executavel.
P5R_STEAM_APPID = "1687950"
GAME_EXE = "P5R.exe"

_PATH_RE = re.compile(r'"path"\s*"([^"]+)"')
_INSTALLDIR_RE = re.compile(r'"installdir"\s*"([^"]+)"')


def _unescape(value: str) -> str:
    # No VDF, barras invertidas vem duplicadas (C:\\Program Files\\Steam).
    return value.replace("\\\\", "\\")


def parse_vdf_paths(text: str) -> list[str]:
    """Extrai todos os valores da chave ``path`` de um libraryfolders.vdf."""
    return [_unescape(m) for m in _PATH_RE.findall(text)]


def parse_acf_installdir(text: str) -> str | None:
    """Extrai ``installdir`` de um appmanifest_*.acf."""
    m = _INSTALLDIR_RE.search(text)
    return _unescape(m.group(1)) if m else None


def find_steam_roots() -> list[Path]:
    """Raizes de instalacao do Steam (registro no Windows + locais comuns)."""
    roots: list[Path] = []

    try:
        import winreg  # disponivel apenas no Windows

        candidates = [
            (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
        ]
        for hive, key, value in candidates:
            try:
                with winreg.OpenKey(hive, key) as k:
                    path, _ = winreg.QueryValueEx(k, value)
                    roots.append(Path(path))
            except OSError:
                pass
    except ImportError:
        pass

    for common in (r"C:\Program Files (x86)\Steam", r"C:\Program Files\Steam"):
        roots.append(Path(common))

    # remove duplicatas preservando a ordem
    seen: set[str] = set()
    unique: list[Path] = []
    for r in roots:
        key = str(r).lower()
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def steam_libraries(steam_root: Path) -> list[Path]:
    """Bibliotecas Steam de uma raiz (a propria raiz + as do libraryfolders.vdf)."""
    libs: list[Path] = [steam_root]
    vdf = steam_root / "steamapps" / "libraryfolders.vdf"
    if vdf.exists():
        for p in parse_vdf_paths(vdf.read_text(encoding="utf-8", errors="ignore")):
            libs.append(Path(p))
    return libs


def looks_like_game_dir(path: Path, exe: str = GAME_EXE) -> bool:
    """True se a pasta contem o executavel do jogo."""
    return (Path(path) / exe).is_file()


def find_game_via_steam(
    steam_roots: list[Path] | None = None,
    appid: str = P5R_STEAM_APPID,
    exe: str = GAME_EXE,
) -> Path | None:
    """Procura a pasta de instalacao do jogo nas bibliotecas Steam."""
    if steam_roots is None:
        steam_roots = find_steam_roots()

    for root in steam_roots:
        if not Path(root).exists():
            continue
        for lib in steam_libraries(Path(root)):
            acf = lib / "steamapps" / f"appmanifest_{appid}.acf"
            if not acf.exists():
                continue
            installdir = parse_acf_installdir(acf.read_text(encoding="utf-8", errors="ignore"))
            if not installdir:
                continue
            candidate = lib / "steamapps" / "common" / installdir
            if candidate.exists():
                return candidate
    return None
