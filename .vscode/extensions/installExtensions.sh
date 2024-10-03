#!/bin/bash

# Verifica se o arquivo de extensões foi fornecido como argumento
if [ $# -ne 1 ]; then
    echo "Uso: $0 arquivo_de_extensoes.json"
    exit 1
fi

EXTENSION_FILE="$1"

# Verifica se o arquivo existe
if [ ! -f "$EXTENSION_FILE" ]; then
    echo "Arquivo $EXTENSION_FILE não encontrado."
    exit 1
fi

# Lê as extensões do arquivo JSON
EXTENSIONS=($(jq -r '.extensions[]' "$EXTENSION_FILE"))

VSCODE_SERVER_ID=$(ls ~/.vscode-server/bin)

# Instala as extensões
for EXTENSION in "${EXTENSIONS[@]}"; do 
    echo "Instalando extensão: $EXTENSION"
    ~/.vscode-server/bin/"$VSCODE_SERVER_ID"/bin/code-server --install-extension "$EXTENSION"
done
