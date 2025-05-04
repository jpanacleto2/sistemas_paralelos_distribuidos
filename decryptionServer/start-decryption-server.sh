#!/bin/bash

VENV_DIR="venv"

# Criar ambiente virtual se não existir
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "Ambiente virtual criado."
fi

# Ativar ambiente virtual
source "$VENV_DIR/bin/activate"

# Instalar dependências
pip install --upgrade pip
pip install -r ../shared/requirements.txt

# Gerar código gRPC
python3 -m grpc_tools.protoc -I../shared --python_out=. --grpc_python_out=. ../shared/crypto.proto

# Rodar o servidor em segundo plano com nohup
nohup python3 decryption_server.py > decryption_server.log 2>&1 &
nohup uvicorn decryption_server_rest:app --host 0.0.0.0 --port 50061 > decryption_server_rest.log 2>&1 &
echo "Servidor iniciado em segundo plano. Log: decryption_server.log"
