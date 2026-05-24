"""Aplica os seeds N5/N4 no banco (idempotente: respeita unique constraints)."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db, get_conn
from seeds import seed_n5, seed_n4


def upsert_nivel(conn, info):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO niveis (codigo, nome, descricao, ordem)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(codigo) DO UPDATE SET
            nome = excluded.nome,
            descricao = excluded.descricao,
            ordem = excluded.ordem
        """,
        (info["codigo"], info["nome"], info["descricao"], info["ordem"]),
    )
    return cur.execute("SELECT id FROM niveis WHERE codigo = ?", (info["codigo"],)).fetchone()[0]


def upsert_topico(conn, nivel_id, ordem, topico):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO topicos (nivel_id, slug, titulo, descricao, ordem)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(nivel_id, slug) DO UPDATE SET
            titulo = excluded.titulo,
            descricao = excluded.descricao,
            ordem = excluded.ordem
        """,
        (nivel_id, topico["slug"], topico["titulo"], topico.get("descricao"), ordem),
    )
    return cur.execute(
        "SELECT id FROM topicos WHERE nivel_id = ? AND slug = ?",
        (nivel_id, topico["slug"]),
    ).fetchone()[0]


def repor_palavras(conn, topico_id, palavras):
    cur = conn.cursor()
    cur.execute("DELETE FROM palavras WHERE topico_id = ?", (topico_id,))
    for i, p in enumerate(palavras, start=1):
        termo, leitura, romaji, significado, classe, ex_jp, ex_pt, nota = p
        cur.execute(
            """
            INSERT INTO palavras
            (topico_id, termo, leitura, romaji, significado_pt, classe, exemplo_jp, exemplo_pt, nota, ordem)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (topico_id, termo, leitura, romaji, significado, classe, ex_jp, ex_pt, nota, i),
        )


def aplicar(modulo):
    conn = get_conn()
    try:
        nivel_id = upsert_nivel(conn, modulo.NIVEL)
        for ordem, topico in enumerate(modulo.TOPICOS, start=1):
            topico_id = upsert_topico(conn, nivel_id, ordem, topico)
            repor_palavras(conn, topico_id, topico["palavras"])
        conn.commit()
        n_palavras = sum(len(t["palavras"]) for t in modulo.TOPICOS)
        print(f"  {modulo.NIVEL['codigo']}: {len(modulo.TOPICOS)} tópicos, {n_palavras} palavras")
    finally:
        conn.close()


def main():
    print("Inicializando banco...")
    init_db()
    print("Aplicando seeds:")
    aplicar(seed_n5)
    aplicar(seed_n4)
    print("Feito.")


if __name__ == "__main__":
    main()
