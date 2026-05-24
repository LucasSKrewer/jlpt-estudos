"""Gerador de quiz de vocabulário no estilo mojigoi (文字・語彙) do JLPT."""

import random


TIPOS = ("leitura", "significado", "termo", "misto")
TIPOS_REAIS = ("leitura", "significado", "termo")

TIPO_LABEL = {
    "leitura": "Leitura do kanji",
    "significado": "Significado em português",
    "termo": "Termo japonês",
    "misto": "Misto (varia entre os tipos)",
}


def _carregar_palavras(conn, nivel_codigo, topico_slug=None):
    """Devolve lista de dicts com palavras do nível (opcionalmente filtradas por tópico)."""
    if topico_slug and topico_slug != "todos":
        rows = conn.execute(
            """
            SELECT p.id, p.termo, p.leitura, p.significado_pt, t.titulo AS topico_titulo
            FROM palavras p
            JOIN topicos t ON t.id = p.topico_id
            JOIN niveis n ON n.id = t.nivel_id
            WHERE n.codigo = ? AND t.slug = ?
            ORDER BY p.id
            """,
            (nivel_codigo, topico_slug),
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT p.id, p.termo, p.leitura, p.significado_pt, t.titulo AS topico_titulo
            FROM palavras p
            JOIN topicos t ON t.id = p.topico_id
            JOIN niveis n ON n.id = t.nivel_id
            WHERE n.codigo = ?
            ORDER BY p.id
            """,
            (nivel_codigo,),
        ).fetchall()
    return [dict(r) for r in rows]


def _tem_kanji(palavra):
    """Há kanji se termo difere da leitura (caso contrário, termo já é só kana)."""
    return palavra["termo"] != palavra["leitura"]


def _gerar_questao_leitura(palavra, pool, n_alternativas=4):
    """Mostra o termo (com kanji); alternativas são leituras de outras palavras."""
    if not _tem_kanji(palavra):
        return None
    candidatos = [p for p in pool if p["id"] != palavra["id"] and p["leitura"] != palavra["leitura"]]
    distratores = random.sample(candidatos, min(n_alternativas - 1, len(candidatos)))
    alternativas = [palavra["leitura"]] + [d["leitura"] for d in distratores]
    random.shuffle(alternativas)
    return {
        "tipo": "leitura",
        "palavra_id": palavra["id"],
        "enunciado": "Como se lê esta palavra?",
        "pergunta": palavra["termo"],
        "alternativas": alternativas,
        "correta": palavra["leitura"],
        "explicacao": f"{palavra['termo']} → {palavra['leitura']} ({palavra['significado_pt']})",
        "topico": palavra.get("topico_titulo"),
    }


def _gerar_questao_significado(palavra, pool, n_alternativas=4):
    """Mostra o termo japonês; alternativas são significados em PT."""
    candidatos = [p for p in pool if p["id"] != palavra["id"] and p["significado_pt"] != palavra["significado_pt"]]
    distratores = random.sample(candidatos, min(n_alternativas - 1, len(candidatos)))
    alternativas = [palavra["significado_pt"]] + [d["significado_pt"] for d in distratores]
    random.shuffle(alternativas)
    return {
        "tipo": "significado",
        "palavra_id": palavra["id"],
        "enunciado": "Qual é o significado desta palavra?",
        "pergunta": palavra["termo"],
        "pergunta_sub": palavra["leitura"] if _tem_kanji(palavra) else None,
        "alternativas": alternativas,
        "correta": palavra["significado_pt"],
        "explicacao": f"{palavra['termo']} ({palavra['leitura']}) → {palavra['significado_pt']}",
        "topico": palavra.get("topico_titulo"),
    }


def _gerar_questao_termo(palavra, pool, n_alternativas=4):
    """Mostra o significado em PT; alternativas são termos em japonês."""
    candidatos = [p for p in pool if p["id"] != palavra["id"] and p["termo"] != palavra["termo"]]
    distratores = random.sample(candidatos, min(n_alternativas - 1, len(candidatos)))
    alternativas = [palavra["termo"]] + [d["termo"] for d in distratores]
    random.shuffle(alternativas)
    return {
        "tipo": "termo",
        "palavra_id": palavra["id"],
        "enunciado": "Qual é o termo japonês correspondente?",
        "pergunta": palavra["significado_pt"],
        "alternativas": alternativas,
        "correta": palavra["termo"],
        "explicacao": f"{palavra['significado_pt']} → {palavra['termo']} ({palavra['leitura']})",
        "topico": palavra.get("topico_titulo"),
    }


_GERADORES = {
    "leitura": _gerar_questao_leitura,
    "significado": _gerar_questao_significado,
    "termo": _gerar_questao_termo,
}


def gerar_quiz(conn, nivel_codigo, tipo, qtd, topico_slug=None):
    """Devolve lista de questões prontas para o quiz.

    Args:
        conn: conexão SQLite
        nivel_codigo: 'N5' ou 'N4'
        tipo: 'leitura' | 'significado' | 'termo' | 'misto'
        qtd: número desejado de questões
        topico_slug: filtro opcional por tópico (ou 'todos')
    """
    if tipo not in TIPOS:
        raise ValueError(f"Tipo inválido: {tipo}")

    pool = _carregar_palavras(conn, nivel_codigo, topico_slug)
    if not pool:
        return []

    palavras_uso = pool[:]
    random.shuffle(palavras_uso)

    questoes = []
    for palavra in palavras_uso:
        if len(questoes) >= qtd:
            break

        if tipo == "misto":
            tipos_aplicaveis = list(TIPOS_REAIS)
            if not _tem_kanji(palavra):
                tipos_aplicaveis.remove("leitura")
            escolhido = random.choice(tipos_aplicaveis)
            questao = _GERADORES[escolhido](palavra, pool)
        else:
            questao = _GERADORES[tipo](palavra, pool)

        if questao is not None:
            questoes.append(questao)

    # Numera as questões a partir de 1
    for i, q in enumerate(questoes, start=1):
        q["numero"] = i

    return questoes
