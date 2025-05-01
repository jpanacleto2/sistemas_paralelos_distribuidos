# Sistema de Criptografia Distribuído com gRPC

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
├── ecryptionServer/     # Servidor gRPC B para decodificação (Python)
└── shared/              # Arquivos compartilhados (proto e requirements)
```

## 1. Web Client (React)

### Configuração e Execução

```bash
cd web

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env # Editar .env para apontar para o API Gateway

# Executar aplicação
npm run dev
```

## 2. API Gateway (Node.js)

### Configuração e Execução

```bash
cd gateway

# Instalar dependências
npm install

# Gerar código gRPC a partir do protofile (Os arquivos _pb2.js e _pb2_grpc.js)
npm run generate

# Configurar variáveis de ambiente
cp .env.example .env # Editar com os endereços dos servidores gRPC

# Executar
npm start
```

## 3. Servidor de Codificação (Python)

### Configuração e Execução

```bash
cd encryptionServer

# Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r ../shared/requirements.txt

# Gerar código gRPC a partir do protofile (Os arquivos _pb2.js e _pb2_grpc.js)
python3 -m grpc_tools.protoc -I../shared --python_out=. --grpc_python_out=. ../shared/crypto.proto

# Executar servidor
python3 encryption_server.py
```

## 4. Servidor de Decodificação (Python)

### Configuração e Execução

```bash
cd decryptionServer

# Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r ../shared/requirements.txt

# Gerar código gRPC a partir do protofile (Os arquivos _pb2.js e _pb2_grpc.js)
python3 -m grpc_tools.protoc -I../shared --python_out=. --grpc_python_out=. ../shared/crypto.proto

# Executar servidor
python3 decryption_server.py
```

## Testando o Sistema

<!-- TODO: Remover essa parte -->

Como ainda não temos virtualização só é possivel testar os componentes independentemente.

### Testando o Web Client

Acesse a interface web em `http://localhost:3000`. Não é possivel testar a funcionalidade.

### Testando o Gateway

Não sei como.

### Testando os Servidores

Utilize os arquivos test.py

```bash
python3 test.py
```