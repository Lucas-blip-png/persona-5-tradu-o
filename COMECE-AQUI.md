# 🎮 Comece aqui

Guia rápido e sem complicação. Escolha o seu caso:

---

## 🕹️ Sou jogador — só quero jogar em português

1. **Tenha o Persona 5 Royal no PC** (Steam) — comprado, de verdade.
2. Baixe o instalador na página de **[Releases](../../releases)** deste projeto:
   o arquivo **`P5R-PTBR-Installer.exe`**.
3. Abra o `.exe`. Ele acha o jogo sozinho — é só **confirmar** e clicar em **Instalar tradução**.
4. Abra o jogo pelo **Reloaded-II** e pronto. 🎉

> Se o instalador disser que falta o **Reloaded-II**, ele te ajuda a baixar. É um programa
> gratuito que "liga" os mods no jogo. Você instala uma vez só.

⚠️ **Importante:** o jogo continua só em inglês até a tradução estar pronta. Este projeto está
em construção — quanto mais texto for traduzido, mais o jogo aparece em português.

---

## ✍️ Quero ajudar a traduzir

Não precisa ser programador. O fluxo é:

1. **Instale o Python** (3.10 ou mais novo) — <https://www.python.org/downloads/>.
2. No terminal, dentro da pasta do projeto:
   ```
   pip install -e ".[dev]"
   ```
3. Extraia o texto do **seu** jogo e gere os arquivos de tradução (passo a passo em
   [`docs/02-extrair-do-jogo.md`](docs/02-extrair-do-jogo.md) e [`docs/03-fluxo-traducao.md`](docs/03-fluxo-traducao.md)).
4. **Traduza**: abra os arquivos `.json` na pasta `translation/`, escreva o texto em português
   no campo `target` e marque `status` como `reviewed`.
5. Gere o mod:
   ```
   p5r-ptbr build
   ```

Dicas de **como traduzir bem** (tom, gírias, voz de cada personagem): veja
[`glossary/guia-de-estilo.md`](glossary/guia-de-estilo.md).

---

## ❓ Dúvidas comuns

- **Isso é oficial?** Não. É um projeto de fã, sem vínculo com a Atlus/Sega.
- **Preciso ter o jogo?** Sim. A tradução não vem com o jogo; ela só se aplica por cima da
  **sua** cópia.
- **É de graça?** Sim. (E a tradução é feita por pessoas, não por tradução automática.)
