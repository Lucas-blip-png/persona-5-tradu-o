"""Integracao com o Reloaded-II: localizar, instalar o mod e ativa-lo.

Parte da automacao do Reloaded-II e best-effort (a estrutura de configuracao
pode variar entre versoes). As funcoes puras (``merge_enabled_mods``) sao
testaveis; as de I/O sao defensivas e degradam para instrucoes manuais.
"""

from __future__ import annotations

import json
import shutil
import sys
import urllib.request
from pathlib import Path

MOD_ID = "p5r.ptbr"
GAME_EXE = "P5R.exe"
RELOADED_LATEST_API = "https://api.github.com/repos/Reloaded-Project/Reloaded-II/releases/latest"


def bundled_mod_dir() -> Path:
    """Pasta do mod a instalar.

    Quando empacotado com PyInstaller, os dados ficam em ``sys._MEIPASS/mod``.
    Em desenvolvimento, usa a pasta ``mod/`` do repositorio.
    """
    base = getattr(sys, "_MEIPASS", None)
    if base:
        candidate = Path(base) / "mod"
        if candidate.exists():
            return candidate
    return Path(__file__).resolve().parents[2] / "mod"


def install_mod_files(mods_dir: Path, mod_src: Path, mod_id: str = MOD_ID) -> Path:
    """Copia o mod para ``<mods_dir>/<mod_id>`` (sobrescreve se existir)."""
    dest = Path(mods_dir) / mod_id
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(mod_src, dest)
    return dest


def merge_enabled_mods(config: dict, mod_ids: list[str]) -> dict:
    """Garante que ``EnabledMods`` contenha os ids informados (puro/testavel)."""
    enabled = list(config.get("EnabledMods", []))
    for mod_id in mod_ids:
        if mod_id not in enabled:
            enabled.append(mod_id)
    config["EnabledMods"] = enabled
    return config


def _app_config_matches_game(config: dict, exe: str) -> bool:
    low = exe.lower()
    for field in ("AppId", "AppLocation", "AppName"):
        value = str(config.get(field, "")).lower()
        if low in value:
            return True
    return False


def enable_mod_in_app_configs(
    reloaded_root: Path, mod_ids: list[str], exe: str = GAME_EXE
) -> list[Path]:
    """Ativa os mods nas configuracoes de app do jogo (best-effort).

    Varre ``AppConfig.json`` sob a pasta do Reloaded-II e, para o app cujo
    executavel bate com ``exe``, adiciona os mods em ``EnabledMods``.
    Retorna os arquivos alterados (vazio se nada foi encontrado).
    """
    changed: list[Path] = []
    for cfg_path in Path(reloaded_root).rglob("AppConfig.json"):
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not _app_config_matches_game(data, exe):
            continue
        merge_enabled_mods(data, mod_ids)
        cfg_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        changed.append(cfg_path)
    return changed


def mod_dependencies(mod_src: Path) -> list[str]:
    """Le ModDependencies do ModConfig.json do mod (para ativar junto)."""
    cfg = Path(mod_src) / "ModConfig.json"
    if not cfg.exists():
        return []
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return list(data.get("ModDependencies", []))


def latest_reloaded_setup_url() -> str | None:
    """URL do Setup.exe da ultima release do Reloaded-II (ou None)."""
    try:
        with urllib.request.urlopen(RELOADED_LATEST_API, timeout=30) as resp:
            data = json.load(resp)
    except Exception:
        return None
    for asset in data.get("assets", []):
        if asset.get("name", "").lower() == "setup.exe":
            return asset.get("browser_download_url")
    return None


def download_file(url: str, dest: Path) -> Path:
    """Baixa um arquivo para ``dest``."""
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as resp, open(dest, "wb") as out:
        shutil.copyfileobj(resp, out)
    return dest
