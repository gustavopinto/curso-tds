import ollama
from .config import OLLAMA_HOST

_client = ollama.Client(host=OLLAMA_HOST)


def ask(model, query, context=[]):
    prompt = (
        f"Use o contexto abaixo para responder a pergunta.\n\n"
        f"Contexto:\n{'---'.join(context)}\n\nPergunta: {query}"
        if context else query
    )
    return _client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )["message"]["content"]
