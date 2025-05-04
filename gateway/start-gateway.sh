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

# Verifica se PM2 está instalado
if ! command -v pm2 &> /dev/null; then
    echo "PM2 não está instalado. Instalando..."
    npm install -g pm2
fi

# Inicia ou reinicia o processo com PM2
if pm2 list | grep -q "$APP_NAME"; then
    echo "Reiniciando $APP_NAME com PM2..."
    pm2 restart "$APP_NAME"
else
    echo "Iniciando $APP_NAME com PM2..."
    pm2 start gateway.js --name "$APP_NAME"
fi

# Salvar configuração para reinício automático no boot (opcional)
pm2 save
