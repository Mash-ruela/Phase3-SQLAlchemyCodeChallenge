
import sqlite3

connection = sqlite3.connect('db/articles.db')
connection.row_factory = sqlite3.Row

def get_connection():
    return connection