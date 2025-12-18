# Python Backend (FastAPI + SQLite)

## Visão Geral

Este projeto implementa uma API REST em Python utilizando FastAPI, responsável por persistência de dados, validação de autenticação JWT e integração com API externa pública.

O backend Python é acessado exclusivamente pelo Node.js (BFF).

## Tecnologias Utilizadas

- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- PyJWT
- Requests
- Uvicorn

## Autenticação

- Autenticação via JWT
- Token recebido via Authorization: Bearer
- JWT validado com chave secreta compartilhada com o Node.js

## Endpoints

Health:
- GET /health

CRUD de itens:
- GET /items
- POST /items
- PUT /items/{id}
- DELETE /items/{id}

API externa pública:
- GET /external/cep/{cep} (ViaCEP)

## Banco de Dados

- SQLite persistente
- Inicialização automática no startup

## Configuração de Ambiente

Recomenda-se criar o arquivo .env a partir do .env_sample.

Variável obrigatória:
- JWT_SECRET (mesmo valor usado no Node.js)

## Docker

Build:
docker build -t python-api .

Run:
docker run -p 8000:8000 --env-file .env python-api

Acesso:
http://localhost:8000
