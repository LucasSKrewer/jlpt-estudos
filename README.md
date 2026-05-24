# JLPT Estudos

Aplicação **Flask local** para estudar vocabulário do **JLPT** (日本語能力試験 — Exame
de Proficiência em Língua Japonesa), com foco nos níveis iniciais **N5** e **N4**.

O sistema organiza o vocabulário em um **roadmap progressivo de tópicos**
temáticos, mostra cada palavra com leitura, romaji, classe gramatical, significado em
português e exemplo de uso, e acompanha o **progresso por palavra**
(`novo` → `estudando` → `aprendido`).

> Projeto de estudos pessoal — focado em vocabulário por enquanto.
> Kanji, gramática, leitura e audição ficam para versões futuras.

## Conteúdo atual

| Nível | Tópicos | Palavras |
|-------|---------|----------|
| N5    | 24      | ~285     |
| N4    | 8       | ~96      |

O conteúdo do **N5** cobre o currículo do JLPT N5 com tópicos progressivos
(saudações → pronomes → números → tempo → família → verbos do dia a dia →
verbos de movimento → adjetivos i/na → cores → comida → lugares → partículas →
demonstrativos → interrogativos → advérbios → corpo → clima → estações →
expressões úteis). O **N4** está com cobertura inicial e cresce conforme o
estudo avança.

## Requisitos

- Python 3.10 ou superior
- Windows, Linux ou macOS

## Instalação

```bash
git clone https://github.com/LucasSKrewer/jlpt-estudos.git
cd jlpt-estudos
pip install -r requirements.txt
```

## Uso

### Primeiro setup

Popular o banco SQLite com os tópicos e palavras do N5 e N4:

```bash
python -m seeds.aplicar_seeds
```

O script é **idempotente**: pode rodar quantas vezes quiser, ele recria os
tópicos e palavras a partir dos seeds em [`seeds/`](seeds/).

### Subir o servidor

```bash
python app.py
```

Abra <http://127.0.0.1:5003> no navegador.

### Fluxo de uso

1. Na **home**, escolha o nível (N5 ou N4).
2. No **roadmap**, veja os tópicos numerados em ordem progressiva, com
   barra de progresso por tópico.
3. Em cada **tópico**, leia as palavras e marque cada uma como `estudando`
   ou `aprendido`. A navegação leva para o próximo tópico no fim da página.
4. Em **Progresso**, acompanhe a distribuição de status e o domínio por
   tópico no nível.

## Estrutura

```
JLPT_Estudos/
├── app.py                  # Flask entry — init_db, registra blueprints
├── config.py               # PORT=5003, DB_PATH, SECRET_KEY
├── database.py             # SQLite + schema + helpers
├── modulos/
│   └── vocabulario/        # Blueprint do módulo de vocabulário
│       └── routes.py
├── seeds/
│   ├── seed_n5.py          # NIVEL + TOPICOS do N5
│   ├── seed_n4.py          # NIVEL + TOPICOS do N4
│   └── aplicar_seeds.py    # Popula o banco (idempotente)
├── templates/
│   ├── base.html
│   ├── home.html
│   └── vocabulario/
│       ├── roadmap.html
│       ├── topico.html
│       └── progresso.html
├── static/style.css
├── requirements.txt
├── INSTRUCOES_PROJETO.md
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Modelo de dados

- **niveis** — `codigo` (N5, N4), `nome`, `descricao`, `ordem`
- **topicos** — agrupa palavras por tema dentro de um nível (`slug`, `titulo`,
  `descricao`, `ordem`)
- **palavras** — `termo` (kanji/kana), `leitura` (hiragana), `romaji`,
  `significado_pt`, `classe` (substantivo, verbo, adjetivo i/na, partícula,
  expressão...), `exemplo_jp`, `exemplo_pt`, `nota`, `ordem`
- **progresso_palavra** — status por palavra (`novo`/`estudando`/`aprendido`)
  + `atualizado_em`

O banco fica em `jlpt.db` (gitignored — é progresso local do usuário).

## Roadmap

- [x] Estrutura Flask + Blueprints + SQLite
- [x] Roadmap progressivo com indicador de progresso por tópico
- [x] Marcação de status por palavra
- [x] Página de progresso por nível
- [x] N5 com 24 tópicos / ~285 palavras
- [x] N4 com 8 tópicos / ~96 palavras
- [ ] Expandir N4 para cobrir o currículo completo
- [ ] Modo quiz por tópico (leitura → escolher significado)
- [ ] Marcar tópicos como "revisar depois"
- [ ] Importação de listas oficiais (CSV/JSON)
- [ ] Eventualmente: kanji, gramática, leitura e audição

## Stack

- Python 3, Flask 3.x, SQLite (stdlib)
- HTML e CSS puro (sem framework, sem JS)

## Licença

[MIT](LICENSE)
