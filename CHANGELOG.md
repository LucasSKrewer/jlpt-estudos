# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.6.0] — 2026-05-24

### Alterado
- **Exercícios agora seguem os formatos oficiais da prova mojigoi (文字・語彙)** do JLPT N5/N4:
  - **漢字読み (kanji yomi)** — mantido: mostra palavra com kanji, pede leitura em hiragana
  - **表記 (hyouki)** — novo: mostra palavra em hiragana, pede a forma em kanji (distratores só com kanji)
  - **文脈規定 (bunmyaku kitei)** — novo: mostra frase com lacuna (　　　) e pede a palavra que preenche; distratores priorizam mesma classe gramatical
  - **Misto** — combina os 3 tipos com filtragem inteligente por aplicabilidade
- Tipos "significado em PT" e "termo a partir de PT" **removidos** (não são formato oficial de prova; só treino casual)
- Página inicial dos exercícios e tela de configuração agora exibem os nomes japoneses dos formatos
- Áudio do botão 🔊 agora vem de `audio_texto` (sempre a leitura ou a frase completa), uniformizado entre os tipos

### Notas
- Todas as questões são geradas **dinamicamente** a partir do vocabulário do banco. Nenhuma questão é cópia de prova ou material oficial — o que reproduzimos é apenas o **formato público** das questões (informação amplamente documentada).
- Para o tipo 4 (言いかえ類義 / sinônimo) faltam dados; fica como roadmap futuro.

## [0.5.0] — 2026-05-24

### Adicionado
- Nova aba **Exercícios** (`/exercicios/`) — quiz no estilo da prova mojigoi (文字・語彙) do JLPT
- 3 tipos de questão (todos formato múltipla escolha com 4 alternativas):
  - **Leitura** (漢字読み) — mostra a palavra com kanji, escolhe a leitura correta em hiragana
  - **Significado** — mostra o termo japonês, escolhe o significado em português
  - **Termo** — mostra o significado em PT, escolhe a palavra japonesa
  - **Misto** — combina os três tipos em uma sessão única
- Quiz **separado por nível** (N5 ou N4) com filtro opcional por tópico e escolha da quantidade de questões (5–50)
- Tela por questão com feedback imediato (alternativa correta destacada em verde matcha, errada em vermelho selo, neutras com opacidade reduzida)
- Página de resultado com pontuação, percentual, mensagem motivacional adaptativa e revisão item a item
- Botão de áudio integrado nas questões de leitura e significado (reaproveita Web Speech API)
- Blueprint `modulos/exercicios/` com `gerador.py` (lógica pura, sem efeitos) e `routes.py` (estado em session Flask)
- Link "Exercícios" no topbar e card 問 na home

## [0.4.0] — 2026-05-24

### Alterado
- **Redesign visual completo em estilo japonês:**
  - Nova paleta: vermelho selo (#bc002d) hi-no-maru, papel washi (#faf6ec) como fundo, sumi (#1a1a1a) como tinta, matcha (#5c7a3e) para N5/aprendido, índigo (#1e3a5f) para N4, dourado (#b8860b) como detalhe
  - Tipografia japonesa com **Noto Serif JP** e **Noto Sans JP** carregadas via Google Fonts; títulos, termos e kanji decorativos em serif
  - Header com selo vermelho 学 (estudo) ao lado do brand "日本語学", linha vermelha + dourada decorativa na base
  - Home com hero em círculo vermelho gigante (200px) contendo 日; cards com kanji decorativo grande (初/中/字) por card e selos coloridos
  - Footer com selo discreto 学 e estilo washi
  - Page heads com border-bottom suave e títulos em serif
  - Cards de palavras com fonte serif no termo, exemplos com borda dourada à esquerda
  - Roadmap numerado em serif japonês
- README: rótulo de licença trocado de "MIT" para "Open Source" (texto do LICENSE continua sendo MIT)

### Corrigido
- `.overview` tinha `grid-template-columns: repeat(3, 1fr) 100%` — a 4ª coluna de 100% empurrava a barra de progresso pra fora, criando scrollbar horizontal espúrio em todas as páginas de roadmap

## [0.3.1] — 2026-05-24

### Alterado
- Aba Kana: tabelas de hiragana e katakana **mescladas em uma única tabela** por seção (gojūon, dakuten, yōon). Cada célula agora mostra hiragana, romaji e katakana lado a lado — antes apareciam em seções separadas, dando a impressão de conteúdo repetido.
- Todas as seções da aba Kana **centralizadas** (intro cards, tabelas, tabela de uso por nível e card de dica) com `max-width: 920px` e `margin: auto`.
- Hiragana destacado em vermelho (cor de accent) e katakana em azul (cor do nível N4) dentro das células — facilita distinguir os dois sistemas de relance.

## [0.3.0] — 2026-05-24

### Adicionado
- Nova aba **Kana** (`/kana/`) com referência completa dos silabários
  - Tabela gojūon (46 caracteres) de hiragana e katakana
  - Tabela dakuten/handakuten (25 caracteres × 2)
  - Tabela yōon — combinações com ゃ/ゅ/ょ (33 × 2)
  - Explicação de quando usar cada sistema (palavras nativas / partículas / terminações vs estrangeirismos / onomatopeias / nomes)
  - Tabela mostrando o uso esperado em cada nível do JLPT (N5 → N3+)
- Cada caractere tem botão 🔊 integrado à Web Speech API (reaproveita `static/audio.js`)
- Blueprint `modulos/kana/` com `routes.py` e `dados.py` (constantes Python)
- Link "Kana" no topbar

### Revisão
- Revisão de segurança (agente revisor-seguranca): 0 findings altos/médios; 3 baixos esperados em app local (secret_key dev, debug=True, sem CSRF)
- QA do módulo kana (agente testador-modulo): 8/8 itens PASS; corrigida chave duplicada `"linha": "n"` em `modulos/kana/dados.py` (linha do ん/ン renomeada para `"nasal"`)

## [0.2.0] — 2026-05-24

### Adicionado
- Botão de áudio 🔊 ao lado de cada termo e de cada frase de exemplo na página do tópico, usando a Web Speech API do navegador
- `static/audio.js`: seleção automática de voz japonesa (preferência por Haruka/Ayumi/Sayaka/Kyoko/Otoya), com taxa de fala ajustada para estudo
- Aviso amigável quando o navegador não tem voz japonesa instalada, com instrução de adicionar o pacote de idiomas do Windows

## [0.1.0] — 2026-05-24

### Adicionado
- Aplicação Flask local com blueprint `vocabulario` (porta 5003)
- Schema SQLite para níveis, tópicos, palavras e progresso por palavra
- Roadmap progressivo por nível com indicador de avanço por tópico
- Página de tópico com termo, leitura, romaji, classe gramatical, significado em PT-BR, exemplo de uso com tradução e notas
- Marcação de status por palavra (`novo`, `estudando`, `aprendido`) com persistência em SQLite
- Página de progresso por nível com distribuição de status e domínio por tópico
- Seeds idempotentes do vocabulário JLPT:
  - **N5**: 24 tópicos cobrindo ~285 palavras (saudações, pronomes, números, tempo, família, verbos do dia a dia, verbos de movimento, adjetivos i/na, cores, comida, lugares, partículas, demonstrativos, interrogativos, advérbios, corpo, clima, estações, expressões úteis)
  - **N4**: 8 tópicos iniciais com ~96 palavras (transporte, profissões, saúde, viagem, tecnologia, emoções, verbos para forma -te, compras)
- CSS sem framework com identidade japonesa
- `INSTRUCOES_PROJETO.md` com estado atual, arquitetura, roadmap de tópicos e próximos passos
- README, LICENSE (MIT) e este CHANGELOG
