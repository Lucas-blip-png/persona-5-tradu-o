# Pasta do mod (Reloaded-II)

Esta é a raiz do mod do Reloaded-II. O `ModConfig.json` define o mod e suas dependências.
O comando `p5r-ptbr build` escreve aqui os arquivos `.msg`/`.flow` traduzidos; o
`p5r-ptbr package` zipa esta pasta para `dist/`.

## Layout esperado pelos emuladores

Com o **Persona Essentials** + **File Emulation Framework**, você fornece arquivos soltos
e os emuladores de **BMD/BF** compilam (`.msg` → `.bmd`, `.flow` → `.bf`) e mesclam por
cima do original **em tempo de execução** — não é preciso reempacotar a CPK.

Os arquivos gerados espelham o **caminho relativo** do arquivo dentro da CPK do jogo. Por
isso é importante preservar a estrutura de pastas ao extrair (veja `docs/02-extrair-do-jogo.md`).

> ⚠️ O nome exato da subpasta que o File Emulation Framework usa para casar cada arquivo
> pode variar conforme a versão do Persona Essentials. **Confirme o layout atual** na
> documentação do Persona Essentials (<https://sewer56.dev/p5rpc.modloader/>) e ajuste, se
> necessário, o destino em `src/p5r_ptbr/build_mod.py` (função `build_mod`, variável `out`).

## O que versionar

- `ModConfig.json` e este `README.md`: **sim**.
- Arquivos `.msg`/`.flow` gerados pelo build: **não** (ignorados pelo `.gitignore`). A fonte
  da verdade é a pasta `translation/` (os JSON). O build é reproduzível a partir dela.
- Fontes editadas (acentos PT-BR): versione o arquivo de fonte modificado se a licença
  permitir; caso contrário, documente como gerá-lo (veja `docs/04-fontes-acentos.md`).
