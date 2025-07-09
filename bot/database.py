import sqlite3
from config import Config


def init_db():
    with sqlite3.connect(Config.SQLITE_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                handle TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                tweet TEXT,
                reply TEXT,
                likes INTEGER,
                retweets INTEGER
            );
            """
        )


def log_to_db(data: dict):
    with sqlite3.connect(Config.SQLITE_PATH) as conn:
        conn.execute(
            """
            INSERT INTO logs (handle, tweet, reply, likes, retweets)
            VALUES (?, ?, ?, ?, ?)
            """,
            (data['handle'], data['tweet'], data['reply'], data['likes'], data['retweets'])
        )