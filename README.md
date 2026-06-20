# Persona 5 Royal — Tradução PT-BR

Tradução em **português brasileiro** de **Persona 5 Royal (PC/Steam)**, feita por fãs, com foco
em **qualidade** (texto fiel e natural — nada de tradução automática genérica).

### 👉 Novo por aqui? Leia o **[COMECE-AQUI.md](COMECE-AQUI.md)**
- 🕹️ **Jogador:** baixe o instalador em **[Releases](../../releases)** (`P5R-PTBR-Installer.exe`), abra e confirme.
- ✍️ **Quer ajudar a traduzir:** veja o passo a passo simples no COMECE-AQUI.

O restante deste README é a parte técnica (o "motor" que produz e empacota a tradução).

> ⚠️ **Projeto de fã, não-oficial.** Sem vínculo com Atlus/Sega. **Nenhum** texto ou asset
> original do jogo é distribuído aqui — você usa os arquivos da **sua** cópia legal. Veja
> [`DISCLAIMER.md`](DISCLAIMER.md).

## Como funciona

```
extrair (.bmd/.bf → .msg) → unidades de tradução (JSON) → revisar/QA → reconstruir (.msg) → mod Reloaded-II
```

Os emuladores do **Persona Essentials / File Emulation Framework** compilam os `.msg`/`.flow`
traduzidos e os mesclam por cima do original **em tempo de execução** — sem reempacotar a CPK.

## Início rápido (tradutor/dev)

```bash
pip install -e ".[dev]"          # instala o toolkit
pip install -e ".[assist]"       # opcional: rascunhos via IA (requer ANTHROPIC_API_KEY)

# 1. extrair o texto da SUA cópia (precisa do AtlusScriptCompiler — veja tools/README.md)
p5r-ptbr extract --input raw/ --dump dump/

# 2. gerar/atualizar as unidades de tradução
p5r-ptbr units --dump dump/ --translation translation/

# 3. (opcional) rascunho de IA  — sempre revisado por humano depois
p5r-ptbr assist --translation translation/ --limit 50

# 4. revisar à mão (edite os JSON em translation/, mude status p/ "reviewed")

# 5. checar qualidade
p5r-ptbr qa --translation translation/ --max-len 42

# 6. reconstruir e empacotar o mod
p5r-ptbr build --dump dump/ --translation translation/ --mod mod/
p5r-ptbr package --mod mod/

p5r-ptbr stats --translation translation/   # progresso
```

## Estrutura

| Caminho | O que é |
|---|---|
| `src/p5r_ptbr/` | o toolkit (parser .msg, unidades, memória, glossário, QA, IA, build) |
| `translation/` | unidades de tradução em JSON (o trabalho versionado) |
| `glossary/` | glossário de termos + guia de estilo + vozes dos personagens |
| `mod/` | esqueleto do mod Reloaded-II (`ModConfig.json`) |
| `tools/` | como obter as ferramentas externas (AtlusScriptCompiler, GFD Studio, Haru Editor) |
| `docs/` | guias passo a passo (instalação, extração, fluxo, fontes, teste, revisão) |
| `dump/` | **(local, ignorado)** arquivos extraídos da sua cópia do jogo |
| `tests/` | testes do toolkit (fixtures sintéticas, sem conteúdo do jogo) |

## Filosofia de tradução

Resumo (detalhes em [`glossary/guia-de-estilo.md`](glossary/guia-de-estilo.md)):
fidelidade ao sentido, naturalidade em PT-BR, adaptação de gírias/trocadilhos, voz por
personagem e consistência via glossário. A IA gera **rascunhos**; **toda linha passa por
revisão humana** antes de virar `reviewed`/`final`.

## Documentação

1. [Instalação](docs/01-instalacao.md)
2. [Extrair do jogo](docs/02-extrair-do-jogo.md)
3. [Fluxo de tradução](docs/03-fluxo-traducao.md)
4. [Fontes e acentos](docs/04-fontes-acentos.md)
5. [Testar no jogo](docs/05-testar-no-jogo.md)
6. [Guia de revisão](docs/06-guia-de-revisao.md)

## Desenvolvimento

```bash
ruff check .
pytest -q
```

## Licença

Código do toolkit sob [MIT](LICENSE). Não cobre nenhum asset/IP de Persona 5 Royal
(Atlus/Sega) — veja [`DISCLAIMER.md`](DISCLAIMER.md).
