# JLPT_Estudos — Sistema de estudos para o JLPT (N5 e N4)

Sistema local em Flask para estudar vocabulário do JLPT (日本語能力試験) com roadmap progressivo e acompanhamento de progresso por palavra.

## Estado atual (2026-05-24)

- **Fase 1 concluída**: estrutura, banco, blueprint vocabulário, templates, seeds N5/N4
- **Fase 2 concluída**: áudio TTS por palavra e por frase de exemplo (Web Speech API, voz do SO)
- **Fase 3 concluída**: aba Kana com hiragana + katakana (gojūon, dakuten, yōon) + uso por nível JLPT; revisada por agentes de segurança e QA
- **Publicado**: [LucasSKrewer/jlpt-estudos](https://github.com/LucasSKrewer/jlpt-estudos) (público, MIT)
- **Servidor**: Flask local, porta **5003**, rodando em background gerenciado pelo Claude
- **Dados**: N5 com 24 tópicos / 285 palavras · N4 com 8 tópicos / 96 palavras
- **Foco**: somente **vocabulário** por enquanto (sem kanji, gramática, leitura)

## Como rodar

```powershell
cd C:\Programas\JLPT_Estudos
python -m seeds.aplicar_seeds   # idempotente — recria os tópicos e palavras
python app.py                    # http://127.0.0.1:5003
```

## Arquitetura

```
JLPT_Estudos/
├── app.py                  # Flask entry, init_db, registra blueprints
├── config.py               # PORT=5003, DB_PATH, SECRET_KEY
├── database.py             # SQLite + schema + helpers
├── modulos/
│   └── vocabulario/        # Blueprint
│       └── routes.py       # roadmap, tópico, marcar status, progresso
├── seeds/
│   ├── seed_n5.py          # NIVEL + TOPICOS (24 tópicos)
│   ├── seed_n4.py          # NIVEL + TOPICOS (8 tópicos)
│   └── aplicar_seeds.py    # script idempotente que popula o banco
├── templates/
│   ├── base.html
│   ├── home.html
│   └── vocabulario/
│       ├── roadmap.html
│       ├── topico.html
│       └── progresso.html
├── static/style.css
└── jlpt.db                 # SQLite (criado no primeiro run)
```

### Modelo de dados

- **niveis**: N5, N4 (`codigo`, `nome`, `descricao`, `ordem`)
- **topicos**: agrupa palavras por tema dentro de um nível (`slug`, `titulo`, `descricao`, `ordem`)
- **palavras**: `termo` (kanji/kana), `leitura` (hiragana), `romaji`, `significado_pt`, `classe` (substantivo, verbo, adjetivo i, adjetivo na, partícula, expressão...), `exemplo_jp`, `exemplo_pt`, `nota`, `ordem`
- **progresso_palavra**: status por palavra — `novo` / `estudando` / `aprendido` + `atualizado_em`

### Fluxo de uso

1. Home `/` → escolher nível (N5 ou N4)
2. `/vocabulario/N5/` → roadmap com tópicos numerados em ordem progressiva, progresso por tópico
3. `/vocabulario/N5/<slug>/` → palavras do tópico com botões para marcar status; navegação para anterior/próximo
4. `/vocabulario/N5/progresso/` → resumo do nível (novo/estudando/aprendido) e domínio por tópico

## Roadmap de aprendizado

### N5 (Iniciante) — vocabulário curricular
1. Saudações e expressões básicas
2. Pronomes e pessoas
3. Números 1-10
4. Números maiores e contadores
5. Dias da semana
6. Tempo, horas e datas
7. Família
8. Verbos do dia a dia
9. Verbos de movimento
10. Adjetivos i (い)
11. Adjetivos na (な)
12. Cores
13. Comida e bebida
14. Lugares comuns
15. Em casa: cômodos e objetos
16. Direções e posições
17. Partículas básicas
18. Demonstrativos (kosoado)
19. Pronomes interrogativos
20. Advérbios de tempo e frequência
21. Corpo humano
22. Clima e natureza
23. Estações e meses
24. Expressões úteis do dia a dia

### N4 (Básico) — vocabulário ampliado
1. Transporte
2. Trabalho e profissões
3. Saúde e médico
4. Viagem
5. Tecnologia e comunicação
6. Emoções e sentimentos
7. Verbos úteis para a forma -te
8. Compras e dinheiro

(N4 está com cobertura inicial — expandir conforme o estudo avança.)

## Decisões

- **Sem dashboard fora dos módulos** — home é só navegação; resumos e estatísticas vivem dentro do módulo vocabulário.
- **Flask + Blueprints + SQLite** — mesmo padrão dos outros projetos IMAC.
- **Status simples (novo/estudando/aprendido)** em vez de SRS — pode evoluir depois.
- **`seeds/aplicar_seeds.py` é idempotente** — pode rodar várias vezes; recria os tópicos/palavras mas mantém o progresso (FK em `progresso_palavra` aponta para `palavra_id`, e como recriamos com mesmas ordens/slugs, o id se renova: o progresso atual é **resetado** ao reseedar; se ficar chato, criar deduplicação por slug+termo).
- **Servidor gerenciado pelo Claude**: roda em background; usuário só dá F5.

## Próximos passos sugeridos

- [ ] Expandir tópicos N4 (faltam ~20 tópicos para cobrir o currículo)
- [ ] Modo quiz simples por tópico (mostrar leitura → escolher significado)
- [ ] Marcar tópicos como "revisar depois"
- [ ] Importar lista oficial JLPT (CSV) para acelerar o seed
- [ ] Eventualmente: kanji, gramática, leituras, audição

## Stack

- Python 3, Flask 3.x, SQLite (stdlib), HTML/CSS puro
- Sem JS no front (formulários POST tradicionais)
