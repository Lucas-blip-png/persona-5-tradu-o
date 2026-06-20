# 05 — Testar no jogo

Este passo roda na **sua máquina**, com o jogo + Reloaded-II instalados (não dá para
automatizar aqui).

## Passos

1. Gere o mod:
   ```bash
   p5r-ptbr build --dump dump/ --translation translation/ --mod mod/
   p5r-ptbr package --mod mod/
   ```
2. No Reloaded-II, instale/atualize o mod (`dist/*.zip`) e ative-o para o P5R, junto com as
   dependências (Persona Essentials, CRI FileSystem V2 Hook, File Emulation Framework).
3. Inicie o jogo pelo Reloaded-II e vá até a cena/menu que você traduziu.

## O que conferir

- O texto traduzido aparece no lugar certo.
- **Acentos** renderizam corretamente (senão, veja `04-fontes-acentos.md`).
- O texto **cabe** na caixa/menu (sem cortar nem estourar). Ajuste quebras com `[n]`.
- As **tags** funcionaram (cores, ícones de botão, nome do falante, pausas).
- Nada quebrou: se o jogo travar ao abrir a cena, normalmente é tag corrompida ou
  arquivo no caminho errado — rode `p5r-ptbr qa` e confira o layout em `mod/README.md`.

## Aprovando

Quando a linha estiver correta **no jogo**, mude o `status` da unidade para `final`.
Antes disso, `reviewed` (revisado no texto) já basta para entrar no build de teste.

## Dica de iteração rápida

Durante o desenvolvimento, o Reloaded-II + File Emulation Framework conseguem ler arquivos
soltos da pasta do mod. Você pode editar o `target`, rodar `build` de novo e reabrir a cena
sem reinstalar tudo.
