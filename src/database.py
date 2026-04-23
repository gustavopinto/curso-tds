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
            CREATE TABLE IF NOT EXISTS docs (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding vector({dim})
            )
        """)
    conn.commit()


def insert(conn, text):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO docs (content, embedding) VALUES (%s, %s)",
            (text, np.array(embed(text))),
        )
    conn.commit()


def search(conn, query, k=3):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT content FROM docs ORDER BY embedding <=> %s LIMIT %s",
            (np.array(embed(query)), k),
        )
        return [r[0] for r in cur.fetchall()]
