"""Extracao: decompila BF/BMD do jogo para .msg usando o AtlusScriptCompiler.

Nao reimplementamos os formatos binarios do jogo. Esta camada apenas orquestra o
AtlusScriptCompiler (ferramenta da comunidade, .NET) que o usuario instala em
``tools/bin`` (veja ``tools/README.md`` e ``tools/bootstrap.*``).
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

TOOLS_BIN = Path("tools/bin")


def find_compiler() -> str | None:
    """Localiza o AtlusScriptCompiler (em tools/bin ou no PATH)."""
    for name in ("AtlusScriptCompiler.exe", "AtlusScriptCompiler"):
        local = TOOLS_BIN / name
        if local.exists():
            return str(local)
    return shutil.which("AtlusScriptCompiler")


def _runner(compiler: str) -> list[str]:
    # Em Linux/macOS o .exe roda via 'dotnet'; no Windows roda direto.
    if compiler.endswith(".exe") and shutil.which("dotnet"):
        return ["dotnet", compiler]
    return [compiler]


def decompile(input_path: Path, output_path: Path, compiler: str | None = None) -> None:
    """Decompila um .bmd/.bf em .msg/.flow. Requer o AtlusScriptCompiler instalado."""
    compiler = compiler or find_compiler()
    if not compiler:
        raise FileNotFoundError(
            "AtlusScriptCompiler nao encontrado. Rode tools/bootstrap.sh (ou .ps1) "
            "ou coloque o binario em tools/bin/. Veja tools/README.md."
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        *_runner(compiler),
        str(input_path),
        "-Decompile",
        "-OutFormat", "v3",
        "-Out", str(output_path),
    ]
    subprocess.run(cmd, check=True)


def decompile_tree(dump_in: Path, dump_out: Path, compiler: str | None = None) -> int:
    """Decompila todos os .bmd/.bf de uma arvore, espelhando os caminhos."""
    compiler = compiler or find_compiler()
    count = 0
    for src in sorted(Path(dump_in).rglob("*")):
        if src.suffix.lower() not in (".bmd", ".bf"):
            continue
        rel = src.relative_to(dump_in)
        ext = ".msg" if src.suffix.lower() == ".bmd" else ".flow"
        decompile(src, Path(dump_out) / rel.with_suffix(ext), compiler)
        count += 1
    return count
