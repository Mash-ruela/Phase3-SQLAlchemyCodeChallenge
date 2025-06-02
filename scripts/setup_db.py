import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db.connection import get_connection
from lib.db.seed import seed_data

def setup_database():
    conn = get_connection()
    with open("lib/db/schema.sql") as f:
        conn.executescript(f.read())
    seed_data()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
