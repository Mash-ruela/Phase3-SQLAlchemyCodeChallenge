import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # lib/db
DB_PATH = os.path.join(BASE_DIR, "articles.db")        # lib/db/articles.db

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn
