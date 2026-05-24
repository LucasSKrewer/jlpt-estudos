from flask import Flask, render_template

from config import PORT, SECRET_KEY
from database import init_db, get_conn
from modulos.vocabulario import bp as vocabulario_bp
from modulos.kana import bp as kana_bp
from modulos.exercicios import bp as exercicios_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.jinja_env.globals["zip"] = zip

    init_db()

    app.register_blueprint(vocabulario_bp, url_prefix="/vocabulario")
    app.register_blueprint(kana_bp, url_prefix="/kana")
    app.register_blueprint(exercicios_bp, url_prefix="/exercicios")

    @app.route("/")
    def home():
        conn = get_conn()
        niveis = conn.execute(
            "SELECT codigo, nome, descricao FROM niveis ORDER BY ordem"
        ).fetchall()
        conn.close()
        return render_template("home.html", niveis=niveis)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=PORT, debug=True)
