from flask import Blueprint, render_template

from .dados import (
    GOJUON_HIRAGANA,
    GOJUON_KATAKANA,
    DAKUTEN_HIRAGANA,
    DAKUTEN_KATAKANA,
    YOON_HIRAGANA,
    YOON_KATAKANA,
    USO_POR_NIVEL,
)


bp = Blueprint("kana", __name__, template_folder="../../templates/kana")


@bp.route("/")
def visao():
    return render_template(
        "kana/visao.html",
        gojuon_hira=GOJUON_HIRAGANA,
        gojuon_kata=GOJUON_KATAKANA,
        dakuten_hira=DAKUTEN_HIRAGANA,
        dakuten_kata=DAKUTEN_KATAKANA,
        yoon_hira=YOON_HIRAGANA,
        yoon_kata=YOON_KATAKANA,
        uso=USO_POR_NIVEL,
    )
