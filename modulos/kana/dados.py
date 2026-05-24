"""Tabelas de hiragana e katakana — caractere, leitura romaji."""


def _matriz(consoante, vogais, romaji):
    return [{"kana": k, "romaji": r} if k else None for k, r in zip(consoante, romaji)]


GOJUON_HIRAGANA = [
    {"linha": "vogais",      "celulas": [("あ", "a"), ("い", "i"), ("う", "u"), ("え", "e"), ("お", "o")]},
    {"linha": "k", "celulas": [("か", "ka"), ("き", "ki"), ("く", "ku"), ("け", "ke"), ("こ", "ko")]},
    {"linha": "s", "celulas": [("さ", "sa"), ("し", "shi"), ("す", "su"), ("せ", "se"), ("そ", "so")]},
    {"linha": "t", "celulas": [("た", "ta"), ("ち", "chi"), ("つ", "tsu"), ("て", "te"), ("と", "to")]},
    {"linha": "n", "celulas": [("な", "na"), ("に", "ni"), ("ぬ", "nu"), ("ね", "ne"), ("の", "no")]},
    {"linha": "h", "celulas": [("は", "ha"), ("ひ", "hi"), ("ふ", "fu"), ("へ", "he"), ("ほ", "ho")]},
    {"linha": "m", "celulas": [("ま", "ma"), ("み", "mi"), ("む", "mu"), ("め", "me"), ("も", "mo")]},
    {"linha": "y", "celulas": [("や", "ya"), (None, None), ("ゆ", "yu"), (None, None), ("よ", "yo")]},
    {"linha": "r", "celulas": [("ら", "ra"), ("り", "ri"), ("る", "ru"), ("れ", "re"), ("ろ", "ro")]},
    {"linha": "w", "celulas": [("わ", "wa"), (None, None), (None, None), (None, None), ("を", "wo")]},
    {"linha": "nasal",  "celulas": [("ん", "n"), (None, None), (None, None), (None, None), (None, None)]},
]

GOJUON_KATAKANA = [
    {"linha": "vogais",      "celulas": [("ア", "a"), ("イ", "i"), ("ウ", "u"), ("エ", "e"), ("オ", "o")]},
    {"linha": "k", "celulas": [("カ", "ka"), ("キ", "ki"), ("ク", "ku"), ("ケ", "ke"), ("コ", "ko")]},
    {"linha": "s", "celulas": [("サ", "sa"), ("シ", "shi"), ("ス", "su"), ("セ", "se"), ("ソ", "so")]},
    {"linha": "t", "celulas": [("タ", "ta"), ("チ", "chi"), ("ツ", "tsu"), ("テ", "te"), ("ト", "to")]},
    {"linha": "n", "celulas": [("ナ", "na"), ("ニ", "ni"), ("ヌ", "nu"), ("ネ", "ne"), ("ノ", "no")]},
    {"linha": "h", "celulas": [("ハ", "ha"), ("ヒ", "hi"), ("フ", "fu"), ("ヘ", "he"), ("ホ", "ho")]},
    {"linha": "m", "celulas": [("マ", "ma"), ("ミ", "mi"), ("ム", "mu"), ("メ", "me"), ("モ", "mo")]},
    {"linha": "y", "celulas": [("ヤ", "ya"), (None, None), ("ユ", "yu"), (None, None), ("ヨ", "yo")]},
    {"linha": "r", "celulas": [("ラ", "ra"), ("リ", "ri"), ("ル", "ru"), ("レ", "re"), ("ロ", "ro")]},
    {"linha": "w", "celulas": [("ワ", "wa"), (None, None), (None, None), (None, None), ("ヲ", "wo")]},
    {"linha": "nasal",  "celulas": [("ン", "n"), (None, None), (None, None), (None, None), (None, None)]},
]


DAKUTEN_HIRAGANA = [
    [("が", "ga"), ("ぎ", "gi"), ("ぐ", "gu"), ("げ", "ge"), ("ご", "go")],
    [("ざ", "za"), ("じ", "ji"), ("ず", "zu"), ("ぜ", "ze"), ("ぞ", "zo")],
    [("だ", "da"), ("ぢ", "ji"), ("づ", "zu"), ("で", "de"), ("ど", "do")],
    [("ば", "ba"), ("び", "bi"), ("ぶ", "bu"), ("べ", "be"), ("ぼ", "bo")],
    [("ぱ", "pa"), ("ぴ", "pi"), ("ぷ", "pu"), ("ぺ", "pe"), ("ぽ", "po")],
]

DAKUTEN_KATAKANA = [
    [("ガ", "ga"), ("ギ", "gi"), ("グ", "gu"), ("ゲ", "ge"), ("ゴ", "go")],
    [("ザ", "za"), ("ジ", "ji"), ("ズ", "zu"), ("ゼ", "ze"), ("ゾ", "zo")],
    [("ダ", "da"), ("ヂ", "ji"), ("ヅ", "zu"), ("デ", "de"), ("ド", "do")],
    [("バ", "ba"), ("ビ", "bi"), ("ブ", "bu"), ("ベ", "be"), ("ボ", "bo")],
    [("パ", "pa"), ("ピ", "pi"), ("プ", "pu"), ("ペ", "pe"), ("ポ", "po")],
]


YOON_HIRAGANA = [
    [("きゃ", "kya"), ("きゅ", "kyu"), ("きょ", "kyo")],
    [("しゃ", "sha"), ("しゅ", "shu"), ("しょ", "sho")],
    [("ちゃ", "cha"), ("ちゅ", "chu"), ("ちょ", "cho")],
    [("にゃ", "nya"), ("にゅ", "nyu"), ("にょ", "nyo")],
    [("ひゃ", "hya"), ("ひゅ", "hyu"), ("ひょ", "hyo")],
    [("みゃ", "mya"), ("みゅ", "myu"), ("みょ", "myo")],
    [("りゃ", "rya"), ("りゅ", "ryu"), ("りょ", "ryo")],
    [("ぎゃ", "gya"), ("ぎゅ", "gyu"), ("ぎょ", "gyo")],
    [("じゃ", "ja"),  ("じゅ", "ju"),  ("じょ", "jo")],
    [("びゃ", "bya"), ("びゅ", "byu"), ("びょ", "byo")],
    [("ぴゃ", "pya"), ("ぴゅ", "pyu"), ("ぴょ", "pyo")],
]

YOON_KATAKANA = [
    [("キャ", "kya"), ("キュ", "kyu"), ("キョ", "kyo")],
    [("シャ", "sha"), ("シュ", "shu"), ("ショ", "sho")],
    [("チャ", "cha"), ("チュ", "chu"), ("チョ", "cho")],
    [("ニャ", "nya"), ("ニュ", "nyu"), ("ニョ", "nyo")],
    [("ヒャ", "hya"), ("ヒュ", "hyu"), ("ヒョ", "hyo")],
    [("ミャ", "mya"), ("ミュ", "myu"), ("ミョ", "myo")],
    [("リャ", "rya"), ("リュ", "ryu"), ("リョ", "ryo")],
    [("ギャ", "gya"), ("ギュ", "gyu"), ("ギョ", "gyo")],
    [("ジャ", "ja"),  ("ジュ", "ju"),  ("ジョ", "jo")],
    [("ビャ", "bya"), ("ビュ", "byu"), ("ビョ", "byo")],
    [("ピャ", "pya"), ("ピュ", "pyu"), ("ピョ", "pyo")],
]


USO_POR_NIVEL = [
    {
        "nivel": "Antes de começar",
        "hiragana": "Obrigatório dominar completamente antes de qualquer prova.",
        "katakana": "Obrigatório dominar completamente antes de qualquer prova.",
    },
    {
        "nivel": "N5",
        "hiragana": "Toda a prova depende de leitura fluente. Maioria das palavras está em hiragana puro ou em kanji com furigana.",
        "katakana": "Empréstimos (パン, テレビ, コーヒー) aparecem em vários blocos. Esperado ler todos os 46 sem hesitar.",
    },
    {
        "nivel": "N4",
        "hiragana": "Já presume domínio total. Aparece em terminações verbais, partículas e palavras sem kanji.",
        "katakana": "Vocabulário estrangeiro mais variado (アパート, スーパー, アルバイト). Combinações longas começam a aparecer.",
    },
    {
        "nivel": "N3 em diante",
        "hiragana": "Domínio absoluto presumido. Furigana fica raro.",
        "katakana": "Termos técnicos e estrangeiros mais complexos (コンピューター, インターネット). Onomatopeias (ドキドキ) também.",
    },
]
