#!/bin/bash

APP_NAME="gateway"

# Instalar dependências
npm install

# Gerar código gRPC a partir do protofile
npm run generate

# Criar .env, se não existir
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Arquivo .env criado a partir de .env.example. Edite-o conforme necessário."
fi

echo "Iniciando $APP_NAME..."
start gateway.js --name "$APP_NAME"
