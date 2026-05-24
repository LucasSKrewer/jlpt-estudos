"""Gerador de quiz no formato oficial da seção mojigoi (文字・語彙) do JLPT.

Implementa os formatos públicos das questões da prova (problem 1-3 do N5/N4):
- 漢字読み (kanji yomi) — dado o kanji, escolher a leitura
- 表記 (hyouki) — dada a leitura, escolher como escrever em kanji
- 文脈規定 (bunmyaku kitei) — preencher lacuna em frase

Todas as questões são geradas dinamicamente a partir do vocabulário do banco;
nenhuma questão é cópia de prova oficial.
"""

import random


TIPOS = ("leitura", "hyouki", "bunmyaku", "misto")
TIPOS_REAIS = ("leitura", "hyouki", "bunmyaku")

TIPO_LABEL = {
    "leitura": "漢字読み — Leitura do kanji",
    "hyouki": "表記 — Escrita em kanji",
    "bunmyaku": "文脈規定 — Preencher a frase",
    "misto": "Misto (varia entre os 3 tipos)",
}

TIPO_DESCRICAO = {
    "leitura": "Mostra a palavra com kanji, você escolhe a leitura em hiragana.",
    "hyouki": "Mostra a palavra em hiragana, você escolhe como escreve em kanji.",
    "bunmyaku": "Mostra uma frase com lacuna (　　　), você escolhe a palavra que preenche.",
    "misto": "Combina os três formatos numa sessão, como na prova real.",
}


def _carregar_palavras(conn, nivel_codigo, topico_slug=None):
    """Devolve lista de dicts com palavras do nível (opcionalmente filtradas por tópico)."""
    if topico_slug and topico_slug != "todos":
        rows = conn.execute(
            """
            SELECT p.id, p.termo, p.leitura, p.romaji, p.significado_pt, p.classe,
                   p.exemplo_jp, p.exemplo_pt, t.titulo AS topico_titulo
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
            SELECT p.id, p.termo, p.leitura, p.romaji, p.significado_pt, p.classe,
                   p.exemplo_jp, p.exemplo_pt, t.titulo AS topico_titulo
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
    """漢字読み — mostra o termo (com kanji), pede a leitura em hiragana.

    Formato oficial: a prova mostra uma frase com palavra sublinhada e pede a
    leitura. Aqui simplificamos para o termo isolado (apropriado para treino).
    """
    if not _tem_kanji(palavra):
        return None
    candidatos = [
        p for p in pool
        if p["id"] != palavra["id"] and p["leitura"] != palavra["leitura"]
    ]
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
        "audio_texto": palavra["leitura"],
        "explicacao": f"{palavra['termo']} → {palavra['leitura']} ({palavra['significado_pt']})",
        "topico": palavra.get("topico_titulo"),
    }


def _gerar_questao_hyouki(palavra, pool, n_alternativas=4):
    """表記 — mostra a leitura em hiragana, pede a forma com kanji.

    Distratores são outras palavras com kanji do mesmo nível, para evitar dica
    visual óbvia (kanji vs hiragana).
    """
    if not _tem_kanji(palavra):
        return None
    candidatos = [
        p for p in pool
        if p["id"] != palavra["id"] and _tem_kanji(p) and p["termo"] != palavra["termo"]
    ]
    if len(candidatos) < n_alternativas - 1:
        return None
    distratores = random.sample(candidatos, n_alternativas - 1)
    alternativas = [palavra["termo"]] + [d["termo"] for d in distratores]
    random.shuffle(alternativas)
    return {
        "tipo": "hyouki",
        "palavra_id": palavra["id"],
        "enunciado": "Qual é a forma correta em kanji desta palavra?",
        "pergunta": palavra["leitura"],
        "alternativas": alternativas,
        "correta": palavra["termo"],
        "audio_texto": palavra["leitura"],
        "explicacao": f"{palavra['leitura']} → {palavra['termo']} ({palavra['significado_pt']})",
        "topico": palavra.get("topico_titulo"),
    }


_LACUNA = "（　　　）"


def _gerar_questao_bunmyaku(palavra, pool, n_alternativas=4):
    """文脈規定 — exibe a frase de exemplo com a palavra substituída por lacuna.

    Só funciona se o termo aparece literalmente no exemplo_jp (verbos
    conjugados/flexões caem fora). Distratores: preferencialmente da mesma
    classe gramatical para a questão ser justa.
    """
    exemplo = palavra.get("exemplo_jp")
    if not exemplo or not palavra["termo"]:
        return None
    if palavra["termo"] not in exemplo:
        return None

    frase_lacuna = exemplo.replace(palavra["termo"], _LACUNA, 1)

    classe = palavra.get("classe") or ""
    mesma_classe = [
        p for p in pool
        if p["id"] != palavra["id"]
        and (p.get("classe") or "") == classe
        and p["termo"] != palavra["termo"]
    ]
    fallback = [
        p for p in pool
        if p["id"] != palavra["id"] and p["termo"] != palavra["termo"]
    ]

    base = mesma_classe if len(mesma_classe) >= n_alternativas - 1 else fallback
    if len(base) < n_alternativas - 1:
        return None
    distratores = random.sample(base, n_alternativas - 1)
    alternativas = [palavra["termo"]] + [d["termo"] for d in distratores]
    random.shuffle(alternativas)

    return {
        "tipo": "bunmyaku",
        "palavra_id": palavra["id"],
        "enunciado": "Qual palavra completa corretamente a frase?",
        "pergunta": frase_lacuna,
        "alternativas": alternativas,
        "correta": palavra["termo"],
        "audio_texto": exemplo,
        "explicacao": (
            f"{exemplo} → {palavra['termo']} ({palavra['leitura']}) — "
            f"{palavra['significado_pt']}"
        ),
        "exemplo_pt": palavra.get("exemplo_pt"),
        "topico": palavra.get("topico_titulo"),
    }


_GERADORES = {
    "leitura": _gerar_questao_leitura,
    "hyouki": _gerar_questao_hyouki,
    "bunmyaku": _gerar_questao_bunmyaku,
}


def _tipos_aplicaveis(palavra):
    """Para uso no modo misto: quais tipos podem ser gerados para esta palavra."""
    aplicaveis = []
    if _tem_kanji(palavra):
        aplicaveis.append("leitura")
        aplicaveis.append("hyouki")
    if palavra.get("exemplo_jp") and palavra["termo"] in (palavra.get("exemplo_jp") or ""):
        aplicaveis.append("bunmyaku")
    return aplicaveis


def gerar_quiz(conn, nivel_codigo, tipo, qtd, topico_slug=None):
    """Gera lista de questões para o quiz.

    Args:
        conn: conexão SQLite
        nivel_codigo: 'N5' ou 'N4'
        tipo: um valor de TIPOS
        qtd: número desejado de questões (o real pode ser menor se faltar material)
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
            aplicaveis = _tipos_aplicaveis(palavra)
            if not aplicaveis:
                continue
            escolhido = random.choice(aplicaveis)
            questao = _GERADORES[escolhido](palavra, pool)
        else:
            questao = _GERADORES[tipo](palavra, pool)

        if questao is not None:
            questoes.append(questao)

    for i, q in enumerate(questoes, start=1):
        q["numero"] = i

    return questoes
