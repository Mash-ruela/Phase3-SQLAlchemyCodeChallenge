from search_db_conn import get_connection

class Article:
    def __init__(self, id=None, title="", author_id=None, magazine_id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE articles SET title=?, author_id=?, magazine_id=? WHERE id=?",
                           (self.title, self.author_id, self.magazine_id, self.id))
        else:
            cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                           (self.title, self.author_id, self.magazine_id))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM articles WHERE title=?", (title,)).fetchone()
        conn.close()
        return cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) if row else None

    @classmethod
    def find_by_author_id(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM articles WHERE author_id=?", (author_id,)).fetchall()
        conn.close()
        return [cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]

    @classmethod
    def find_by_magazine_id(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM articles WHERE magazine_id=?", (magazine_id,)).fetchall()
        conn.close()
        return [cls(id=row[0], title=row[1], author_id=row[2], magazine_id=row[3]) for row in rows]
