import sqlite3
from flask import g, current_app, Flask

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e = None):
    db: sqlite3.Connection = g.pop('db', None)

    if db is not None:
        db.close()

def register_db(app: Flask):
    app.teardown_appcontext(close_db)

def init_db():
    db = get_db()
    db.execute("CREATE TABLE IF NOT EXISTS account(id INTEGER PRIMARY KEY, amount INTEGER, action TEXT, time TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS idempotence_key(id INTEGER PRIMARY KEY, key TEXT, time TEXT)")