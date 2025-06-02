import sqlite3

def get_connection():
    conn = sqlite3.connect("your_database.db")
    conn.row_factory = sqlite3.Row  # enables row["column_name"] access
    return conn