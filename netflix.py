import argparse
from src.config import LLM_MODEL, EMBED_MODEL
from src.database import connect, setup, search_filmes
from src.embeddings import embed
from src.llm import ask


def main():
    parser = argparse.ArgumentParser(description="RAG com Ollama e pgvector")
    parser.add_argument("--model", default=LLM_MODEL, help="Modelo LLM do Ollama")
    args = parser.parse_args()

    conn = connect()
    setup(conn, len(embed("warmup")))

    print(f"RAG | LLM: {args.model} | Embeddings: {EMBED_MODEL}")
    print("Digite /quit para sair.\n")

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not line:
            continue
        if line == "/quit":
            break

        ctx = search_filmes(conn, line)
        if ctx:
            print("\n<inicio>contexto recuperado</inicio>")
            for i, doc in enumerate(ctx, 1):
                print(f"  [{i}] {doc[:120]}{'...' if len(doc) > 120 else ''}")
            print("<fim>contexto recuperado</fim>\n")
        print(ask(args.model, line, ctx))

    conn.close()


if __name__ == "__main__":
    main()
