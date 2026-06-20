# Ferramentas externas

O toolkit **orquestra** ferramentas da comunidade (não as reimplementa). Você as instala
em `tools/bin/` (ignorado pelo Git) ou no `PATH`. Os scripts `bootstrap.sh` / `bootstrap.ps1`
ajudam a baixá-las.

| Ferramenta | Para quê | Onde obter |
|---|---|---|
| **AtlusScriptCompiler** | decompilar/compilar `BF`/`BMD` ↔ `.msg`/`.flow` | repositório da comunidade (AtlusScriptToolchain) |
| **GFD Studio** | editar fontes (adicionar acentos) e texturas | repositório da comunidade |
| **Haru Editor** | editar tabelas `.tbl` (itens/skills/personas) | <https://gamebanana.com/tools/21451> |
| **CriPakTools / YACpkTool / PuyoTools** | extrair `.cpk` | repositórios da comunidade |

> Os links e versões mudam com o tempo. Comece pelo guia de modding do P5R PC:
> <https://docs.shrinefox.com/getting-started/persona-5-royal-pc-mod-support>.

## Fixar versões

Para builds reproduzíveis, anote aqui a versão exata que a equipe está usando:

- AtlusScriptCompiler: `vX.Y.Z`
- GFD Studio: `vX.Y.Z`
- Haru Editor: `vX.Y.Z`

## Requisitos

- **AtlusScriptCompiler** é .NET. No Windows roda direto; em Linux/macOS, instale o
  **.NET runtime** (`dotnet`) — o toolkit chama `dotnet AtlusScriptCompiler.exe`
  automaticamente quando detecta o `.exe` fora do Windows.
