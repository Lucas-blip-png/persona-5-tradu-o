# 04 — Fontes e acentos do PT-BR

O português brasileiro usa caracteres acentuados (á à â ã é ê í ó ô õ ú ç) que a fonte
original do jogo pode **não** conter. Sem isso, esses caracteres aparecem em branco ou
como caixas. Por isso, parte do trabalho de localização é **adicionar os glifos à fonte**.

## Ferramenta

Use o **GFD Studio** (ferramenta da comunidade) para abrir e editar as fontes (formato GFD)
e os atlas de glifos do jogo, além de converter texturas (`.gnf` ↔ `.png`).

## Roteiro geral

1. Localize o(s) arquivo(s) de fonte na CPK (geralmente em `font/...`).
2. Abra no GFD Studio e verifique quais glifos acentuados já existem.
3. Adicione os glifos faltantes (acentos e `ç`), idealmente reaproveitando a base latina
   da própria fonte para manter o estilo.
4. Exporte a fonte modificada e coloque-a na pasta do mod, no caminho que espelha o
   original (veja `mod/README.md`).
5. Teste no jogo: escreva uma linha com todos os acentos e confira no diálogo e nos menus.

## Dicas

- Telas estreitas (caixas de diálogo/menus) têm limite de largura. Use `p5r-ptbr qa
  --max-len N` para sinalizar linhas longas e ajuste com `[n]`.
- Algumas telas usam **texto em textura** (imagem), não fonte: esse texto precisa ser
  redesenhado como imagem (também via GFD Studio / editor de imagem).
- Mantenha um arquivo de teste com pangrama PT-BR para validar a fonte rapidamente, por
  exemplo: "Um pequeno jabuti xereta viu dez cegonhas felizes."
