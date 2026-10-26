import string
import random
from flask import Flask, request, redirect, render_template, abort
import database as db

app = Flask(__name__)

# Base62: caracteres usados para gerar o código curto
ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6


def generate_code() -> str:
    """Gera código aleatório de 6 caracteres. Repete se houver colisão."""
    while True:
        code = "".join(random.choices(ALPHABET, k=CODE_LENGTH))
        if not db.code_exists(code):
            return code


def is_valid_url(url: str) -> bool:
    """Validação simples: precisa começar com http:// ou https://."""
    return url.startswith(("http://", "https://"))


@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None
    error = None

    if request.method == "POST":
        original = request.form.get("url", "").strip()

        if not original:
            error = "Informe uma URL."
        elif not is_valid_url(original):
            error = "URL inválida. Use http:// ou https://"
        else:
            code = generate_code()
            db.create_short_url(code, original)
            short_url = request.host_url + code

    return render_template("index.html", short_url=short_url, error=error)


@app.route("/<code>")
def redirect_to_original(code):
    """Redireciona para a URL original e incrementa o contador."""
    row = db.get_url_by_code(code)
    if row is None:
        abort(404)
    db.increment_clicks(code)
    return redirect(row["original"], code=302)


@app.route("/stats/<code>")
def stats(code):
    """Endpoint simples para consultar estatísticas (JSON)."""
    row = db.get_url_by_code(code)
    if row is None:
        abort(404)
    return {
        "code": row["code"],
        "original": row["original"],
        "clicks": row["clicks"],
        "created_at": row["created_at"],
    }


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)
