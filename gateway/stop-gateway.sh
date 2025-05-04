#!/bin/bash

APP_NAME="gateway"

# Verifica se PM2 está instalado
if ! command -v pm2 &> /dev/null; then
    echo "PM2 não está instalado."
    exit 1
fi

# Verifica se o processo está rodando
if pm2 list | grep -q "$APP_NAME"; then
    echo "Parando $APP_NAME com PM2..."
    pm2 stop "$APP_NAME"
    pm2 delete "$APP_NAME"
else
    echo "Nenhum processo chamado $APP_NAME encontrado no PM2."
fi
