from lib.db.connection import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Jane Doe",))
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Weekly", "Technology"))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", (
        "The Future of AI", 1, 1
    ))

    conn.commit()
    conn.close()
    print("✅ Seed data inserted.")

if __name__ == "__main__":
    seed_data()
