"""Empacota a pasta do mod em um .zip pronto para o Reloaded-II."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path


def package_mod(mod_dir: Path, dist_dir: Path = Path("dist")) -> Path:
    mod_dir = Path(mod_dir)
    config = mod_dir / "ModConfig.json"
    if not config.exists():
        raise FileNotFoundError(f"ModConfig.json nao encontrado em {mod_dir}")

    mod_id = json.loads(config.read_text(encoding="utf-8")).get("ModId", "p5r.ptbr")
    dist_dir = Path(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dist_dir / f"{mod_id}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(mod_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(mod_dir).as_posix())

    return zip_path
