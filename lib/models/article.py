from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (self.title, self.author_id, self.magazine_id)
        )
        self.id = cursor.lastrowid
        conn.commit()

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        row = cursor.fetchone()
        if row:
            return cls(id=row["id"], title=row["title"], author_id=row["author_id"], magazine_id=row["magazine_id"])
        return None

    def author(self):
        from lib.models.author import Author  # local import to avoid circular import
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from lib.models.magazine import Magazine  # local import
        return Magazine.find_by_id(self.magazine_id)