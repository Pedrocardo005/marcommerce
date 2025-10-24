#!/bin/bash

VENV_DIR="env"
REQUIREMENTS_FILE="requirements.txt"
PROJECT_DIR="code"

# 1. VERIFICA E CRIA O AMBIENTE VIRTUAL
echo "Verificando o ambiente virtual ($VENV_DIR)..."

# O 'if' verifica se o diretório do ambiente virtual NÃO existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Ambiente virtual não encontrado. Criando e configurando..."

    # Cria o ambiente virtual
    # Usando 'python3' ou 'python' dependendo da sua configuração
    python3 -m venv $VENV_DIR

    # Ativa o ambiente para instalar as dependências
    . $VENV_DIR/bin/activate

    # Instala as dependências (se o arquivo requirements.txt existir)
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo "Instalando dependências de $REQUIREMENTS_FILE..."
        pip install -r $REQUIREMENTS_FILE
    else
        echo "Aviso: O arquivo $REQUIREMENTS_FILE não foi encontrado. Nenhuma dependência instalada."
    fi

    # Desativa o ambiente (para garantir que a próxima ativação seja limpa)
    deactivate

    echo "Ambiente virtual configurado com sucesso!"
else
    echo "Ambiente virtual ($VENV_DIR) já existe."
fi

# 2. ATIVAÇÃO DO AMBIENTE VIRTUAL E EXECUÇÃO DO SERVIDOR
# Ativa o ambiente virtual (garantindo que esteja ativo para rodar o Django)
. "$VENV_DIR/bin/activate"
echo "Ambiente virtual ativado."

# Executa o servidor Django
echo "Iniciando o servidor Django..."
python manage.py runserver 0.0.0.0:8080