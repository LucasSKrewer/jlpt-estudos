import sqlite3
from contextlib import contextmanager
from config import DB_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS niveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    descricao TEXT,
    ordem INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS topicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nivel_id INTEGER NOT NULL,
    slug TEXT NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT,
    ordem INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (nivel_id) REFERENCES niveis(id),
    UNIQUE(nivel_id, slug)
);

CREATE TABLE IF NOT EXISTS palavras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topico_id INTEGER NOT NULL,
    termo TEXT NOT NULL,
    leitura TEXT NOT NULL,
    romaji TEXT,
    significado_pt TEXT NOT NULL,
    classe TEXT,
    exemplo_jp TEXT,
    exemplo_pt TEXT,
    nota TEXT,
    ordem INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (topico_id) REFERENCES topicos(id)
);

CREATE TABLE IF NOT EXISTS progresso_palavra (
    palavra_id INTEGER PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'novo',
    atualizado_em TEXT,
    FOREIGN KEY (palavra_id) REFERENCES palavras(id)
);

CREATE INDEX IF NOT EXISTS idx_topicos_nivel ON topicos(nivel_id, ordem);
CREATE INDEX IF NOT EXISTS idx_palavras_topico ON palavras(topico_id, ordem);
"""


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def db_cursor():
    conn = get_conn()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    finally:
        conn.close()


def init_db():
    with db_cursor() as cur:
        cur.executescript(SCHEMA)
