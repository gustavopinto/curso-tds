# RAG com Ollama e pgvector

Sistema de recomendação de filmes via linha de comando usando Retrieval-Augmented Generation (RAG), com Ollama como LLM e embeddings, e PostgreSQL com pgvector como banco vetorial.

## Arquitetura

```
rag.py                      # ponto de entrada — CLI e loop de conversa
ingest.py                   # ingestão do catálogo de filmes
catalogo_de_filmes.json     # catálogo com 125 filmes nacionais e internacionais
src/
  config.py                 # variáveis de ambiente e constantes
  database.py               # conexão, setup e operações vetoriais
  embeddings.py             # geração de embeddings via Ollama
  llm.py                    # geração de respostas via Ollama
```

## Pré-requisitos

- [Ollama](https://ollama.com) instalado e rodando localmente
- Docker e Docker Compose
- Python 3.10+

## Setup

**1. Configurar o `.env`:**

O arquivo `.env` já vem com os valores padrão. Edite se necessário:

```ini
LLM_MODEL=llama3.2
DATABASE_URL=postgresql://rag:rag@localhost:5432/rag
OLLAMA_HOST=http://localhost:11434

PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin
```

**2. Baixar os modelos no Ollama:**

```bash
ollama pull embeddinggemma
ollama pull llama3.2
```

**3. Subir os serviços:**

```bash
docker compose up -d
```

pgAdmin disponível em `http://localhost:8080`. Para conectar ao banco, use host `db`, porta `5432`, usuário e senha `rag`.

**4. Instalar dependências Python:**

```bash
pip install -r requirements.txt
```

## Uso

**Ingestão:**

```bash
python ingest.py catalogo_de_filmes.json            # importa todos os filmes
python ingest.py catalogo_de_filmes.json --limit 10 # importa apenas 10
python ingest.py --clear                            # limpa a base
```

**Conversar:**

```bash
python netflix.py
python netflix.py --model mistral   # sobrescreve o LLM_MODEL do .env
```

Digite `/quit` para sair.

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `LLM_MODEL` | `llama3.2` | Modelo LLM usado nas respostas |
| `DATABASE_URL` | `postgresql://rag:rag@localhost:5432/rag` | URL de conexão com o PostgreSQL |
| `OLLAMA_HOST` | `http://localhost:11434` | Host do serviço Ollama |
| `PGADMIN_EMAIL` | `admin@admin.com` | Login do pgAdmin |
| `PGADMIN_PASSWORD` | `admin` | Senha do pgAdmin |
