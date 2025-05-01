# README - Sistema de Criptografia Distribuído com gRPC

## Visão Geral do Projeto

Este projeto implementa um sistema distribuído de criptografia usando:
- **Web Client**: Interface React para usuários
- **API Gateway**: Stub gRPC que recebe requisições HTTP e roteia para os servidores gRPC
- **Servidor de Codificação**: Serviço gRPC para criptografar texto usando cifra de Vigenère
- **Servidor de Decodificação**: Serviço gRPC para descriptografar texto usando cifra de Vigenère

## Pré-requisitos

- Node.js
- Python

## Estrutura do Projeto

```
├── web/                 # Aplicação React
├── gateway/             # Stub gRPC (Node.js)
├── encryptionServer/    # Servidor gRPC A para codificação (Python)
└── decryptionServer/    # Servidor gRPC B para decodificação (Python)
```

## 1. Web Client (React)

### Configuração e Execução

```bash
cd web

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env para apontar para o API Gateway

# Executar aplicação
npm run dev
```

**Variáveis de Ambiente:**
```
REACT_APP_API_URL=http://localhost:8080
```

## 2. API Gateway (Node.js)

### Configuração e Execução

```bash
cd api-gateway

# Instalar dependências
npm install

# Gerar código gRPC a partir do protofile
npm run generate

# Configurar variáveis de ambiente
cp .env.example .env
# Editar com os endereços dos servidores gRPC

# Executar
npm start
```

**Variáveis de Ambiente:**
```
ENCRYPT_SERVER_ADDRESS=localhost:50051
DECRYPT_SERVER_ADDRESS=localhost:50052
PORT=8080
```

## 3. Servidor de Codificação (Python)

### Configuração e Execução

```bash
cd encryption-server

# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Gerar código gRPC
python -m grpc_tools.protoc -I../shared --python_out=. --grpc_python_out=. ../shared/crypto.proto

# Executar servidor
python server.py
```

**Variáveis de Ambiente (opcional):**
```
SERVER_PORT=50051
```

## 4. Servidor de Decodificação (Python)

### Configuração e Execução

```bash
cd decryption-server

# Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Gerar código gRPC
python -m grpc_tools.protoc -I../shared --python_out=. --grpc_python_out=. ../shared/crypto.proto

# Executar servidor
python server.py
```

**Variáveis de Ambiente (opcional):**
```
SERVER_PORT=50052
```

## Execução com Docker (Opcional)

```bash
# Na raiz do projeto
docker-compose up --build
```

## Ordem Recomendada para Iniciar os Serviços

1. Servidor de Codificação (`encryption-server`)
2. Servidor de Decodificação (`decryption-server`)
3. API Gateway (`api-gateway`)
4. Web Client (`web-client`)

## Testando o Sistema

1. Acesse a interface web em `http://localhost:3000`
2. Ou teste diretamente a API:

```bash
# Codificar
curl -X POST http://localhost:8080/encrypt \
  -H "Content-Type: application/json" \
  -d '{"text": "HELLO", "key": "KEY"}'

# Decodificar
curl -X POST http://localhost:8080/decrypt \
  -H "Content-Type: application/json" \
  -d '{"text": "RIJVS", "key": "KEY"}'
```