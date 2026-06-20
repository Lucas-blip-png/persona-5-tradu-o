# Baixa as ferramentas externas para tools/bin/ (Windows / PowerShell).
#
# As ferramentas da comunidade nao tem URLs estaveis garantidas; edite as
# variaveis abaixo com a versao/URL que sua equipe fixou (veja tools/README.md)
# antes de rodar. Este script NAO baixa nada do jogo.
$ErrorActionPreference = "Stop"

$BinDir = Join-Path $PSScriptRoot "bin"
New-Item -ItemType Directory -Force -Path $BinDir | Out-Null

# Preencha com a release fixada (exemplo):
# $AtlusScriptUrl = "https://github.com/.../AtlusScriptCompiler.zip"

if (-not $AtlusScriptUrl) {
    Write-Host "Defina `$AtlusScriptUrl (e demais URLs) em tools/bootstrap.ps1."
    Write-Host "Veja tools/README.md para onde obter cada ferramenta."
    exit 1
}

Write-Host "Baixando AtlusScriptCompiler para $BinDir ..."
$Zip = Join-Path $BinDir "atlusscript.zip"
Invoke-WebRequest -Uri $AtlusScriptUrl -OutFile $Zip
Expand-Archive -Path $Zip -DestinationPath $BinDir -Force
Remove-Item $Zip
Write-Host "Pronto. Verifique com: dir $BinDir"
