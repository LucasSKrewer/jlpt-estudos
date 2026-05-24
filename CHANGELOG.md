# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

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
