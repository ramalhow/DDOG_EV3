#!/bin/bash

# Navega para a pasta libs
cd lib

# Itera sobre todos os arquivos .py na pasta libs
for arquivo_py in *.py; do
    # Verifica se encontrou algum arquivo .py
    if [ "$arquivo_py" = "*.py" ]; then
        echo "Nenhum arquivo .py encontrado na pasta libs"
        exit 0
    fi
    
    # Extrai o nome do arquivo sem a extensão
    nome_base=$(basename "$arquivo_py" .py)
    
    # Define o nome do arquivo de output
    arquivo_mpy="../${nome_base}.mpy"
    
    echo "Compilando: $arquivo_py -> $arquivo_mpy"
    
    # Executa o comando mpy-cross
    mpy-cross -O2 "$arquivo_py" -o "$arquivo_mpy"
    
    # Verifica se a compilação foi bem sucedida
    if [ $? -eq 0 ]; then
        echo "✓ Sucesso: $arquivo_mpy"
    else
        echo "✗ Erro ao compilar: $arquivo_py"
    fi
done

echo "Compilação concluída!"