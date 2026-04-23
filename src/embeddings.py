import ollama
from .config import EMBED_MODEL, OLLAMA_HOST

_client = ollama.Client(host=OLLAMA_HOST)


def embed(text):
    return _client.embeddings(model=EMBED_MODEL, prompt=text)["embedding"]
