import numpy as np
import psycopg2
from pgvector.psycopg2 import register_vector
from .config import DB_URL
from .embeddings import embed


def connect():
    return psycopg2.connect(DB_URL)


def setup(conn, dim):
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()
    register_vector(conn)
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS filmes (
                id INTEGER PRIMARY KEY,
                titulo TEXT,
                titulo_original TEXT,
                sinopse TEXT,
                data_lancamento DATE,
                generos TEXT[],
                diretor TEXT,
                pais TEXT,
                idioma TEXT,
                nota_imdb REAL,
                duracao_min INTEGER,
                embedding vector({dim})
            )
        """)
    conn.commit()


def insert_filme(conn, filme):
    texto = (
        f"{filme['titulo']}. {filme['sinopse']} "
        f"Gêneros: {', '.join(filme['generos'])}. Diretor: {filme['diretor']}. "
        f"País: {filme['pais']}."
    )
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO filmes
               (id, titulo, titulo_original, sinopse, data_lancamento, generos,
                diretor, pais, idioma, nota_imdb, duracao_min, embedding)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (id) DO NOTHING""",
            (
                filme["id"], filme["titulo"], filme.get("titulo_original"),
                filme["sinopse"], filme["data_lancamento"], filme["generos"],
                filme["diretor"], filme["pais"], filme["idioma"],
                filme["nota_imdb"], filme["duracao_min"],
                np.array(embed(texto)),
            ),
        )
    conn.commit()


def search_filmes(conn, query, k=3):
    with conn.cursor() as cur:
        cur.execute(
            """SELECT titulo, sinopse, nota_imdb, diretor, generos, data_lancamento
               FROM filmes ORDER BY embedding <=> %s LIMIT %s""",
            (np.array(embed(query)), k),
        )
        return [
            f"{r[0]} (dir. {r[3]}, {r[5].year}, nota {r[2]}): {r[1]}"
            for r in cur.fetchall()
        ]
