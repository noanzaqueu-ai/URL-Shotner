import sqlite3
from datetime import datetime

DB_PATH = "encurtador.db"


def get_connection():
    """Abre conexão com o SQLite. row_factory permite acessar colunas por nome."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria a tabela se não existir. Chamado uma vez na inicialização."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                code       TEXT UNIQUE NOT NULL,
                original   TEXT NOT NULL,
                clicks     INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


def create_short_url(code: str, original: str) -> None:
    """Insere um novo short link."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO urls (code, original, created_at) VALUES (?, ?, ?)",
            (code, original, datetime.utcnow().isoformat()),
        )
        conn.commit()


def get_url_by_code(code: str):
    """Busca uma URL pelo código. Retorna None se não existir."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM urls WHERE code = ?", (code,)
        ).fetchone()
    return row


def increment_clicks(code: str) -> None:
    """Incrementa o contador de cliques."""
    with get_connection() as conn:
        conn.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE code = ?", (code,)
        )
        conn.commit()


def code_exists(code: str) -> bool:
    """Verifica colisão de código."""
    return get_url_by_code(code) is not None
