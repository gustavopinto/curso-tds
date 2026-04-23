import os
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = "embeddinggemma"
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")
DB_URL = os.getenv("DATABASE_URL", "postgresql://rag:rag@localhost:5432/rag")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
