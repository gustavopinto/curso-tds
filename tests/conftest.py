import pytest
from src.config import LLM_MODEL, OLLAMA_HOST
from src.database import connect, setup
from src.embeddings import embed
from tests.ollama_judge import OllamaJudge


@pytest.fixture(scope="session")
def judge():
    return OllamaJudge(model=LLM_MODEL, host=OLLAMA_HOST)


@pytest.fixture(scope="session")
def db():
    conn = connect()
    setup(conn, len(embed("warmup")))
    yield conn
    conn.close()
