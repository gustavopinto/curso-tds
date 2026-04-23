import argparse
from src.database import connect, setup, insert
from src.embeddings import embed


def main():
    parser = argparse.ArgumentParser(description="Ingestão de documentos para o RAG")
    parser.add_argument("files", nargs="+", help="Arquivos .txt para ingerir")
    parser.add_argument("--clear", action="store_true", help="Limpa a base antes de ingerir")
    args = parser.parse_args()

    conn = connect()
    setup(conn, len(embed("warmup")))

    if args.clear:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM docs")
        conn.commit()
        print("Base limpa.")

    for path in args.files:
        chunks = [c.strip() for c in open(path).read().split("\n\n") if c.strip()]
        for chunk in chunks:
            insert(conn, chunk)
        print(f"{path}: {len(chunks)} chunks adicionados.")

    conn.close()


if __name__ == "__main__":
    main()
