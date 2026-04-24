import argparse
import json
from src.database import connect, setup, insert_filme
from src.embeddings import embed


def main():
    parser = argparse.ArgumentParser(description="Ingestão do catálogo de filmes")
    parser.add_argument("arquivo", nargs="?", help="Arquivo .json para ingerir")
    parser.add_argument("--clear", action="store_true", help="Limpa a base de filmes")
    parser.add_argument("--limit", type=int, default=None, metavar="N",
                        help="Máximo de filmes a importar")
    args = parser.parse_args()

    conn = connect()
    setup(conn, len(embed("warmup")))

    if args.clear:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM filmes")
        conn.commit()
        print("Base limpa.")
        conn.close()
        return

    if not args.arquivo:
        parser.error("informe um arquivo .json para ingerir")

    data = json.load(open(args.arquivo))
    filmes = data["filmes"] if isinstance(data, dict) else data
    if args.limit:
        filmes = filmes[:args.limit]

    total = len(filmes)
    for i, filme in enumerate(filmes, 1):
        insert_filme(conn, filme)
        print(f"  [{i}/{total}] {filme['titulo']}")

    print(f"\n{total} filmes adicionados.")
    conn.close()


if __name__ == "__main__":
    main()
