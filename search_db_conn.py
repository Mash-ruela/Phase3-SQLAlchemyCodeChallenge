import sqlite3
import os

def get_connection():
    db_path = os.path.join("db", "articles.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # <-- This line enables dict-like row access
    return conn
