# Instalador gráfico (.exe) — um clique

Assistente para o **jogador final**: escolhe a pasta do jogo, confirma e o instalador
aplica a tradução. Pensado para quem não quer mexer com linha de comando.

> ⚠️ **O instalador aplica uma tradução pronta — ele não cria a tradução.** O texto em
> PT-BR é produzido com o toolkit (raiz do repositório, `docs/03-fluxo-traducao.md`) e
> empacotado no `mod/`. O instalador leva esse `mod/` para dentro do Reloaded-II.

## O que ele faz

1. **Detecta o Persona 5 Royal** instalado via Steam (`P5R.exe`) — ou você aponta a pasta.
2. Se você não tiver o **Reloaded-II**, ele baixa o instalador oficial e orienta a instalação.
3. Copia o mod da tradução para a pasta `Mods/` do Reloaded-II.
4. **Tenta ativar** o mod para o jogo (best-effort). As dependências (Persona Essentials,
   File Emulation Framework, CRI FileSystem V2 Hook) são resolvidas pelo próprio Reloaded-II.
5. Pronto: é só abrir o jogo pelo Reloaded-II.

> A automação do Reloaded-II é **best-effort** (a estrutura de config muda entre versões).
> Quando o instalador não consegue ativar sozinho, ele mostra exatamente o que clicar no
> Reloaded-II (adicionar o jogo + ativar o mod "Tradução PT-BR").

## Rodar a partir do código (dev)

```bash
python -m p5r_ptbr_installer        # a partir da pasta installer/ no PYTHONPATH
# ou:
python installer/run_installer.py
```

Requer Python com **tkinter** (incluso no Python oficial do Windows/macOS).

## Gerar o .exe

O `.exe` é gerado automaticamente pelo **GitHub Actions** (workflow `Build installer (.exe)`),
em `windows-latest`, e publicado como artefato. Para gerar localmente no Windows:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name P5R-PTBR-Installer --add-data "mod;mod" --paths installer installer/run_installer.py
# resultado em dist/P5R-PTBR-Installer.exe
```

## Estrutura

| Arquivo | O que é |
|---|---|
| `p5r_ptbr_installer/steam.py` | detecção do jogo via Steam (testável) |
| `p5r_ptbr_installer/reloaded.py` | instalar/ativar o mod, baixar o Reloaded-II (testável) |
| `p5r_ptbr_installer/wizard.py` | interface gráfica (tkinter) |
| `run_installer.py` | ponto de entrada para o PyInstaller |
