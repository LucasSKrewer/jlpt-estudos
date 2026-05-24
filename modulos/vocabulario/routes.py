from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, abort, flash

from database import get_conn

bp = Blueprint("vocabulario", __name__, template_folder="../../templates/vocabulario")


def _nivel_por_codigo(conn, codigo):
    return conn.execute(
        "SELECT id, codigo, nome, descricao FROM niveis WHERE codigo = ?", (codigo,)
    ).fetchone()


def _topicos_do_nivel(conn, nivel_id):
    return conn.execute(
        """
        SELECT t.id, t.slug, t.titulo, t.descricao, t.ordem,
               COUNT(p.id) AS total_palavras,
               SUM(CASE WHEN pr.status = 'aprendido' THEN 1 ELSE 0 END) AS aprendidas
        FROM topicos t
        LEFT JOIN palavras p ON p.topico_id = t.id
        LEFT JOIN progresso_palavra pr ON pr.palavra_id = p.id
        WHERE t.nivel_id = ?
        GROUP BY t.id
        ORDER BY t.ordem
        """,
        (nivel_id,),
    ).fetchall()


@bp.route("/")
def index():
    return redirect(url_for("vocabulario.roadmap", nivel="N5"))


@bp.route("/<nivel>/")
def roadmap(nivel):
    conn = get_conn()
    nivel_row = _nivel_por_codigo(conn, nivel)
    if not nivel_row:
        conn.close()
        abort(404)

    topicos = _topicos_do_nivel(conn, nivel_row["id"])

    niveis = conn.execute("SELECT codigo, nome FROM niveis ORDER BY ordem").fetchall()
    conn.close()

    total = sum(t["total_palavras"] for t in topicos)
    aprendidas = sum((t["aprendidas"] or 0) for t in topicos)
    pct = round((aprendidas / total) * 100, 1) if total else 0.0

    return render_template(
        "vocabulario/roadmap.html",
        nivel=nivel_row,
        niveis=niveis,
        topicos=topicos,
        total=total,
        aprendidas=aprendidas,
        pct=pct,
    )


@bp.route("/<nivel>/<slug>/")
def topico(nivel, slug):
    conn = get_conn()
    nivel_row = _nivel_por_codigo(conn, nivel)
    if not nivel_row:
        conn.close()
        abort(404)

    topico_row = conn.execute(
        "SELECT id, slug, titulo, descricao FROM topicos WHERE nivel_id = ? AND slug = ?",
        (nivel_row["id"], slug),
    ).fetchone()
    if not topico_row:
        conn.close()
        abort(404)

    palavras = conn.execute(
        """
        SELECT p.id, p.termo, p.leitura, p.romaji, p.significado_pt, p.classe,
               p.exemplo_jp, p.exemplo_pt, p.nota,
               COALESCE(pr.status, 'novo') AS status
        FROM palavras p
        LEFT JOIN progresso_palavra pr ON pr.palavra_id = p.id
        WHERE p.topico_id = ?
        ORDER BY p.ordem, p.id
        """,
        (topico_row["id"],),
    ).fetchall()

    vizinhos = conn.execute(
        """
        SELECT slug, titulo, ordem FROM topicos
        WHERE nivel_id = ? ORDER BY ordem
        """,
        (nivel_row["id"],),
    ).fetchall()
    conn.close()

    anterior = proximo = None
    for i, v in enumerate(vizinhos):
        if v["slug"] == slug:
            if i > 0:
                anterior = vizinhos[i - 1]
            if i < len(vizinhos) - 1:
                proximo = vizinhos[i + 1]
            break

    total = len(palavras)
    aprendidas = sum(1 for p in palavras if p["status"] == "aprendido")
    pct = round((aprendidas / total) * 100, 1) if total else 0.0

    return render_template(
        "vocabulario/topico.html",
        nivel=nivel_row,
        topico=topico_row,
        palavras=palavras,
        anterior=anterior,
        proximo=proximo,
        total=total,
        aprendidas=aprendidas,
        pct=pct,
    )


@bp.route("/palavra/<int:palavra_id>/status", methods=["POST"])
def marcar_status(palavra_id):
    novo_status = request.form.get("status", "novo")
    if novo_status not in ("novo", "estudando", "aprendido"):
        abort(400)

    conn = get_conn()
    palavra = conn.execute(
        """
        SELECT p.id, t.slug AS topico_slug, n.codigo AS nivel_codigo
        FROM palavras p
        JOIN topicos t ON t.id = p.topico_id
        JOIN niveis n ON n.id = t.nivel_id
        WHERE p.id = ?
        """,
        (palavra_id,),
    ).fetchone()
    if not palavra:
        conn.close()
        abort(404)

    agora = datetime.now().isoformat(timespec="seconds")
    conn.execute(
        """
        INSERT INTO progresso_palavra (palavra_id, status, atualizado_em)
        VALUES (?, ?, ?)
        ON CONFLICT(palavra_id) DO UPDATE SET status = excluded.status, atualizado_em = excluded.atualizado_em
        """,
        (palavra_id, novo_status, agora),
    )
    conn.commit()
    conn.close()

    return redirect(
        url_for(
            "vocabulario.topico",
            nivel=palavra["nivel_codigo"],
            slug=palavra["topico_slug"],
        )
        + f"#palavra-{palavra_id}"
    )


@bp.route("/<nivel>/progresso/")
def progresso(nivel):
    conn = get_conn()
    nivel_row = _nivel_por_codigo(conn, nivel)
    if not nivel_row:
        conn.close()
        abort(404)

    topicos = _topicos_do_nivel(conn, nivel_row["id"])

    distribuicao = conn.execute(
        """
        SELECT COALESCE(pr.status, 'novo') AS status, COUNT(*) AS qtd
        FROM palavras p
        JOIN topicos t ON t.id = p.topico_id
        LEFT JOIN progresso_palavra pr ON pr.palavra_id = p.id
        WHERE t.nivel_id = ?
        GROUP BY status
        """,
        (nivel_row["id"],),
    ).fetchall()

    niveis = conn.execute("SELECT codigo, nome FROM niveis ORDER BY ordem").fetchall()
    conn.close()

    contagem = {"novo": 0, "estudando": 0, "aprendido": 0}
    for r in distribuicao:
        contagem[r["status"]] = r["qtd"]
    total = sum(contagem.values())

    return render_template(
        "vocabulario/progresso.html",
        nivel=nivel_row,
        niveis=niveis,
        topicos=topicos,
        contagem=contagem,
        total=total,
    )
