"""
Raw SQLite DB helper for direct SQL operations.
"""

import sqlite3
from config import Config

def get_db():
    """Return a SQLite connection with dict row access."""
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create tables if they don't exist."""
    conn = get_db()
    cur = conn.cursor()

    # Users table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    # Issues table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        type TEXT NOT NULL,
        created_by TEXT NOT NULL,
        assigned_to TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()
