"""CLI do toolkit: p5r-ptbr <comando>.

Comandos:
  extract   Decompila .bmd/.bf do jogo para .msg (via AtlusScriptCompiler).
  units     Gera/atualiza as unidades de traducao (JSON) a partir dos .msg.
  assist    Gera rascunhos via IA (opcional; requer P5R_AI_API_URL/KEY/MODEL).
  qa        Roda as checagens de qualidade.
  build     Reconstroi os .msg traduzidos dentro da pasta do mod.
  package   Empacota a pasta do mod em um .zip para o Reloaded-II.
  stats     Mostra o progresso da traducao por status.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from . import __version__
from .glossary import Glossary
from .units import load_units

DEFAULT_DUMP = Path("dump")
DEFAULT_TRANSLATION = Path("translation")
DEFAULT_MOD = Path("mod")
DEFAULT_GLOSSARY = Path("glossary/glossario.pt-br.csv")


def _load_glossary(path: Path) -> Glossary | None:
    return Glossary.load(path) if Path(path).exists() else None


def _all_units(translation_dir: Path) -> list:
    units = []
    for jp in sorted(Path(translation_dir).rglob("*.json")):
        units.extend(load_units(jp))
    return units


def cmd_extract(args: argparse.Namespace) -> int:
    from .extract import decompile_tree

    count = decompile_tree(Path(args.input), Path(args.dump))
    print(f"Decompilados {count} arquivo(s) para {args.dump}/")
    return 0


def cmd_units(args: argparse.Namespace) -> int:
    from .build_units import build_units

    stats = build_units(Path(args.dump), Path(args.translation), use_memory=not args.no_memory)
    print(
        f"Arquivos: {stats['files']} | unidades: {stats['units']} | "
        f"reaproveitadas da TM: {stats['reused']}"
    )
    return 0


def cmd_assist(args: argparse.Namespace) -> int:
    from . import assist

    if not assist.available():
        print(
            "IA indisponivel. Defina as variaveis de ambiente P5R_AI_API_URL, "
            "P5R_AI_API_KEY e P5R_AI_MODEL. (O fluxo manual continua funcionando.)"
        )
        return 1

    glossary = _load_glossary(args.glossary)
    cfg = assist.load_config(Path("."), glossary)
    total = 0
    for jp in sorted(Path(args.translation).rglob("*.json")):
        from .units import save_units

        units = load_units(jp)
        n = assist.draft_units(units, cfg, limit=args.limit)
        if n:
            rel = jp.relative_to(args.translation).as_posix().removesuffix(".json")
            save_units(jp, rel, units)
            total += n
        if args.limit is not None and total >= args.limit:
            break
    print(f"Rascunhos gerados: {total} (status='draft' — revise antes de aprovar)")
    return 0


def cmd_qa(args: argparse.Namespace) -> int:
    from .qa import run_qa

    units = _all_units(args.translation)
    rep = run_qa(units, _load_glossary(args.glossary), max_visible_len=args.max_len)
    print(f"Total: {rep.total} | faltam traduzir: {rep.untranslated}")
    print(f"Tags divergentes: {len(rep.tag_mismatches)}")
    print(f"Alvo vazio (aprovado): {len(rep.missing_target)}")
    print(f"Linhas longas: {len(rep.too_long)}")
    print(f"Avisos de glossario: {len(rep.glossary)}")
    for key in rep.tag_mismatches[:10]:
        print(f"  [tag] {key}")
    for key, viol in rep.glossary[:10]:
        print(f"  [glo] {key}: {viol}")
    return 0 if rep.ok else 2


def cmd_build(args: argparse.Namespace) -> int:
    from .build_mod import build_mod

    stats = build_mod(Path(args.dump), Path(args.translation), Path(args.mod))
    print(
        f"Arquivos gerados: {stats['files']} | mensagens traduzidas: "
        f"{stats['messages']} | ignoradas: {stats['skipped']}"
    )
    return 0


def cmd_package(args: argparse.Namespace) -> int:
    from .package_mod import package_mod

    zip_path = package_mod(Path(args.mod))
    print(f"Mod empacotado em: {zip_path}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    units = _all_units(args.translation)
    counts = Counter(u.status for u in units)
    total = len(units) or 1
    print(f"Unidades totais: {len(units)}")
    for status in ("untranslated", "draft", "reviewed", "final"):
        n = counts.get(status, 0)
        print(f"  {status:12s}: {n:6d} ({100 * n / total:5.1f}%)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="p5r-ptbr", description="Toolkit de localizacao PT-BR de P5R")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    pe = sub.add_parser("extract", help="Decompila .bmd/.bf -> .msg")
    pe.add_argument("--input", required=True, help="Pasta com os .bmd/.bf extraidos da CPK")
    pe.add_argument("--dump", default=str(DEFAULT_DUMP))
    pe.set_defaults(func=cmd_extract)

    pu = sub.add_parser("units", help="Gera/atualiza unidades de traducao")
    pu.add_argument("--dump", default=str(DEFAULT_DUMP))
    pu.add_argument("--translation", default=str(DEFAULT_TRANSLATION))
    pu.add_argument("--no-memory", action="store_true", help="Nao aplicar a memoria de traducao")
    pu.set_defaults(func=cmd_units)

    pa = sub.add_parser("assist", help="Gera rascunhos via IA (opcional)")
    pa.add_argument("--translation", default=str(DEFAULT_TRANSLATION))
    pa.add_argument("--glossary", default=str(DEFAULT_GLOSSARY))
    pa.add_argument("--limit", type=int, default=None, help="Maximo de rascunhos a gerar")
    pa.set_defaults(func=cmd_assist)

    pq = sub.add_parser("qa", help="Checagens de qualidade")
    pq.add_argument("--translation", default=str(DEFAULT_TRANSLATION))
    pq.add_argument("--glossary", default=str(DEFAULT_GLOSSARY))
    pq.add_argument("--max-len", type=int, default=None, help="Limite de caracteres por linha")
    pq.set_defaults(func=cmd_qa)

    pb = sub.add_parser("build", help="Reconstroi .msg traduzidos no mod")
    pb.add_argument("--dump", default=str(DEFAULT_DUMP))
    pb.add_argument("--translation", default=str(DEFAULT_TRANSLATION))
    pb.add_argument("--mod", default=str(DEFAULT_MOD))
    pb.set_defaults(func=cmd_build)

    pp = sub.add_parser("package", help="Empacota o mod em .zip")
    pp.add_argument("--mod", default=str(DEFAULT_MOD))
    pp.set_defaults(func=cmd_package)

    ps = sub.add_parser("stats", help="Progresso por status")
    ps.add_argument("--translation", default=str(DEFAULT_TRANSLATION))
    ps.set_defaults(func=cmd_stats)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
