#!/usr/bin/env bash
# Baixa as ferramentas externas para tools/bin/ (Linux/macOS).
#
# As ferramentas da comunidade nao tem URLs estaveis garantidas; edite as
# variaveis abaixo com a versao/URL que sua equipe fixou (veja tools/README.md)
# antes de rodar. Este script NAO baixa nada do jogo.
set -euo pipefail

BIN_DIR="$(cd "$(dirname "$0")" && pwd)/bin"
mkdir -p "$BIN_DIR"

# Preencha com a release fixada (exemplo):
# ATLUSSCRIPT_URL="https://github.com/.../AtlusScriptCompiler.zip"

if [[ -z "${ATLUSSCRIPT_URL:-}" ]]; then
  echo "Defina ATLUSSCRIPT_URL (e demais URLs) em tools/bootstrap.sh ou no ambiente."
  echo "Veja tools/README.md para onde obter cada ferramenta."
  exit 1
fi

echo "Baixando AtlusScriptCompiler para $BIN_DIR ..."
curl -L "$ATLUSSCRIPT_URL" -o "$BIN_DIR/atlusscript.zip"
unzip -o "$BIN_DIR/atlusscript.zip" -d "$BIN_DIR"
rm -f "$BIN_DIR/atlusscript.zip"
echo "Pronto. Verifique com: ls $BIN_DIR"
