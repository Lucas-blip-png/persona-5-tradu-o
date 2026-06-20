# 01 — Instalação (jogar com mods no P5R PC)

Esta tradução roda como um **mod do Reloaded-II** na versão de **PC (Steam)** de
Persona 5 Royal. Você precisa ter o jogo legalmente.

## Pré-requisitos do jogador

1. **Persona 5 Royal (PC/Steam)** instalado.
2. **Reloaded-II** — gerenciador de mods. Baixe em <https://reloaded-project.github.io/Reloaded-II/>.
3. Pelos mods/dependências essenciais da comunidade (instale pelo navegador de mods do
   Reloaded-II e ative para o P5R):
   - **Persona Essentials** / `p5rpc.modloader` (carrega arquivos soltos sem reempacotar a CPK)
   - **CRI FileSystem V2 Hook**
   - **File Emulation Framework** (emuladores de BF/BMD/TBL — compilam em tempo de execução)

> Referência da comunidade (atualizada): guia de modding do P5R PC em
> <https://docs.shrinefox.com/getting-started/persona-5-royal-pc-mod-support> e a
> documentação do Persona Essentials em <https://sewer56.dev/p5rpc.modloader/>.

## Instalando a tradução (mod pronto)

1. Pegue o `.zip` do mod (gerado por `p5r-ptbr package`, em `dist/`).
2. No Reloaded-II, arraste o `.zip` para a lista de mods (ou extraia na pasta `Mods/`).
3. Ative o mod para o Persona 5 Royal, junto com as dependências acima.
4. Inicie o jogo pelo Reloaded-II.

Se as dependências estiverem ativas, os emuladores compilam os `.msg`/`.flow` traduzidos
e os mesclam por cima do texto original — sem editar os arquivos do jogo.

## Pré-requisitos para quem vai traduzir/desenvolver

- **Python 3.10+**
- Instale o toolkit em modo de desenvolvimento:
  ```bash
  pip install -e ".[dev]"
  ```
- Opcional (rascunhos de IA): defina as variáveis `P5R_AI_API_URL`, `P5R_AI_API_KEY` e `P5R_AI_MODEL` (provedor à sua escolha).
- Ferramentas externas de extração/fontes: veja `tools/README.md`.
