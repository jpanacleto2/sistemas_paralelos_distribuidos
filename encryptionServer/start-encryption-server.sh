#!/bin/bash

# Instalar dependências
pip install --upgrade pip
pip install -r ../shared/requirements.txt

# Gerar código gRPC
python3 -m grpc_tools.protoc -I../shared --python_out=. --grpc_python_out=. ../shared/crypto.proto

# Rodar o servidor em segundo plano com nohup
nohup python3 encryption_server.py > encryption_server.log 2>&1 &
nohup uvicorn encryption_server_rest:app --host 0.0.0.0 --port 50061 > encryption_server_rest.log 2>&1 &
echo "Servidor iniciado em segundo plano. Log: encryption_server.log"
