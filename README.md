# RAG com Ollama e pgvector

Aplicação de Retrieval-Augmented Generation (RAG) via linha de comando, usando Ollama como LLM e embeddings, e PostgreSQL com pgvector como banco vetorial.

## Arquitetura

```
rag.py              # ponto de entrada — CLI e loop de conversa
ingest.py           # ingestão de documentos
src/
  config.py         # variáveis de ambiente e constantes
  database.py       # conexão, setup e operações vetoriais
  embeddings.py     # geração de embeddings via Ollama
  llm.py            # geração de respostas via Ollama
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
```

**2. Baixar os modelos no Ollama:**

```bash
ollama pull embeddinggemma
ollama pull llama3.2
```

**3. Subir o banco de dados:**

```bash
docker compose up -d
```

**4. Instalar dependências Python:**

```bash
pip install -r requirements.txt
```

## Uso

**Ingerir documentos:**

```bash
python ingest.py doc1.txt doc2.txt
python ingest.py --clear doc1.txt   # limpa a base antes de ingerir
```

**Conversar:**

```bash
python rag.py
python rag.py --model mistral       # sobrescreve o LLM_MODEL do .env
```

Digite `/quit` para sair.

## Variáveis de ambiente

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| `LLM_MODEL` | `llama3.2` | Modelo LLM usado nas respostas |
| `DATABASE_URL` | `postgresql://rag:rag@localhost:5432/rag` | URL de conexão com o PostgreSQL |
| `OLLAMA_HOST` | `http://localhost:11434` | Host do serviço Ollama |
