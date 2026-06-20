# 02 — Extrair o texto do seu jogo

> ⚠️ **Você precisa ter o jogo legalmente.** Este repositório **não** contém nenhum texto
> ou asset original de Persona 5 Royal. Você extrai os arquivos da **sua** cópia e eles
> ficam só na sua máquina (a pasta `dump/` é ignorada pelo Git).

## Visão geral do fluxo

```
CPK do jogo ──(extrair)──> .bmd / .bf ──(decompilar)──> .msg / .flow ──> dump/
```

## 1. Extrair os arquivos da CPK

O texto fica dentro dos arquivos `.cpk` (CRIWARE), principalmente em arquivos `.bmd`
(mensagens) e `.bf` (flowscript), além de tabelas `.tbl`. Use uma ferramenta da
comunidade para extrair a CPK, por exemplo:

- **CriPakTools / YACpkTool / PuyoTools** — extração de `.cpk`.

Copie os `.bmd`/`.bf` que você quer traduzir para uma pasta de entrada (ex.: `raw/`),
preservando a estrutura de pastas (isso importa: o caminho relativo é usado para casar o
arquivo modificado com o original em tempo de execução).

## 2. Decompilar BMD/BF para texto editável

Instale o **AtlusScriptCompiler** (veja `tools/README.md` ou rode `tools/bootstrap.sh`).
Depois:

```bash
p5r-ptbr extract --input raw/ --dump dump/
```

Isso decompila todos os `.bmd`→`.msg` e `.bf`→`.flow` espelhando os caminhos em `dump/`.

## 3. Gerar as unidades de tradução

```bash
p5r-ptbr units --dump dump/ --translation translation/
```

Cada arquivo vira um JSON em `translation/` com uma unidade por mensagem. A partir daqui,
veja `03-fluxo-traducao.md`.

## Tabelas (.tbl) — nomes de itens/skills/persona

Tabelas binárias (nomes de itens, habilidades, etc.) são melhor editadas com o
**Haru Editor** (editor de TBL da comunidade). Exporte os textos, traduza seguindo o
glossário e gere o `.tbl` modificado para a pasta do mod.
