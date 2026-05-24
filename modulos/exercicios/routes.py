from flask import Blueprint, render_template, redirect, url_for, request, session, abort, flash

from database import get_conn
from .gerador import gerar_quiz, TIPO_LABEL


bp = Blueprint("exercicios", __name__, template_folder="../../templates/exercicios")


def _niveis_disponiveis(conn):
    return conn.execute(
        "SELECT codigo, nome, descricao FROM niveis ORDER BY ordem"
    ).fetchall()


def _validar_nivel(conn, codigo):
    row = conn.execute("SELECT id, codigo, nome FROM niveis WHERE codigo = ?", (codigo,)).fetchone()
    return row


@bp.route("/")
def inicio():
    conn = get_conn()
    niveis = _niveis_disponiveis(conn)
    contagens = {
        r["codigo"]: r["qtd"]
        for r in conn.execute(
            """
            SELECT n.codigo, COUNT(p.id) AS qtd
            FROM niveis n
            LEFT JOIN topicos t ON t.nivel_id = n.id
            LEFT JOIN palavras p ON p.topico_id = t.id
            GROUP BY n.codigo
            """
        ).fetchall()
    }
    conn.close()
    return render_template("exercicios/inicio.html", niveis=niveis, contagens=contagens)


@bp.route("/<nivel>/")
def configurar(nivel):
    conn = get_conn()
    nivel_row = _validar_nivel(conn, nivel)
    if not nivel_row:
        conn.close()
        abort(404)

    topicos = conn.execute(
        """
        SELECT t.slug, t.titulo, COUNT(p.id) AS qtd_palavras
        FROM topicos t
        LEFT JOIN palavras p ON p.topico_id = t.id
        WHERE t.nivel_id = ?
        GROUP BY t.id
        ORDER BY t.ordem
        """,
        (nivel_row["id"],),
    ).fetchall()

    total_palavras = sum(t["qtd_palavras"] for t in topicos)
    conn.close()

    return render_template(
        "exercicios/configurar.html",
        nivel=nivel_row,
        topicos=topicos,
        total_palavras=total_palavras,
        tipos=TIPO_LABEL,
    )


@bp.route("/<nivel>/iniciar", methods=["POST"])
def iniciar(nivel):
    conn = get_conn()
    nivel_row = _validar_nivel(conn, nivel)
    if not nivel_row:
        conn.close()
        abort(404)

    tipo = request.form.get("tipo", "misto")
    if tipo not in TIPO_LABEL:
        conn.close()
        abort(400)

    try:
        qtd = int(request.form.get("qtd", "10"))
    except ValueError:
        conn.close()
        abort(400)
    qtd = max(5, min(qtd, 50))

    topico = request.form.get("topico", "todos") or "todos"

    questoes = gerar_quiz(conn, nivel_row["codigo"], tipo, qtd, topico)
    conn.close()

    if not questoes:
        flash("Não há palavras suficientes para gerar um quiz com essa configuração.", "info")
        return redirect(url_for("exercicios.configurar", nivel=nivel_row["codigo"]))

    session["quiz"] = {
        "nivel": nivel_row["codigo"],
        "tipo": tipo,
        "topico": topico,
        "questoes": questoes,
        "respostas": {},
    }
    session.modified = True

    return redirect(url_for("exercicios.questao", nivel=nivel_row["codigo"], idx=1))


def _carregar_quiz(nivel):
    quiz = session.get("quiz")
    if not quiz or quiz.get("nivel") != nivel:
        return None
    return quiz


@bp.route("/<nivel>/quiz/<int:idx>/")
def questao(nivel, idx):
    quiz = _carregar_quiz(nivel)
    if not quiz:
        return redirect(url_for("exercicios.configurar", nivel=nivel))

    questoes = quiz["questoes"]
    if idx < 1 or idx > len(questoes):
        return redirect(url_for("exercicios.resultado", nivel=nivel))

    questao_atual = questoes[idx - 1]
    resposta = quiz["respostas"].get(str(idx))

    return render_template(
        "exercicios/questao.html",
        nivel=nivel,
        questao=questao_atual,
        idx=idx,
        total=len(questoes),
        resposta=resposta,
        tipo_label=TIPO_LABEL.get(quiz["tipo"]),
    )


@bp.route("/<nivel>/responder/<int:idx>", methods=["POST"])
def responder(nivel, idx):
    quiz = _carregar_quiz(nivel)
    if not quiz:
        return redirect(url_for("exercicios.configurar", nivel=nivel))

    questoes = quiz["questoes"]
    if idx < 1 or idx > len(questoes):
        return redirect(url_for("exercicios.resultado", nivel=nivel))

    resposta = request.form.get("alternativa", "")
    quiz["respostas"][str(idx)] = resposta
    session["quiz"] = quiz
    session.modified = True

    return redirect(url_for("exercicios.questao", nivel=nivel, idx=idx))


@bp.route("/<nivel>/proxima/<int:idx>/")
def proxima(nivel, idx):
    quiz = _carregar_quiz(nivel)
    if not quiz:
        return redirect(url_for("exercicios.configurar", nivel=nivel))

    total = len(quiz["questoes"])
    proximo_idx = idx + 1
    if proximo_idx > total:
        return redirect(url_for("exercicios.resultado", nivel=nivel))
    return redirect(url_for("exercicios.questao", nivel=nivel, idx=proximo_idx))


@bp.route("/<nivel>/resultado/")
def resultado(nivel):
    quiz = _carregar_quiz(nivel)
    if not quiz:
        return redirect(url_for("exercicios.configurar", nivel=nivel))

    questoes = quiz["questoes"]
    respostas = quiz["respostas"]

    acertos = 0
    detalhamento = []
    for q in questoes:
        idx = q["numero"]
        resp = respostas.get(str(idx))
        correto = resp == q["correta"]
        if correto:
            acertos += 1
        detalhamento.append({
            "numero": idx,
            "questao": q,
            "resposta_usuario": resp,
            "correto": correto,
        })

    total = len(questoes)
    pct = round((acertos / total) * 100, 1) if total else 0.0

    return render_template(
        "exercicios/resultado.html",
        nivel=nivel,
        acertos=acertos,
        total=total,
        pct=pct,
        detalhamento=detalhamento,
        tipo_label=TIPO_LABEL.get(quiz["tipo"]),
    )


@bp.route("/<nivel>/limpar/", methods=["POST"])
def limpar(nivel):
    session.pop("quiz", None)
    return redirect(url_for("exercicios.configurar", nivel=nivel))
