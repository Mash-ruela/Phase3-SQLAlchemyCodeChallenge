from lib.db.connection import get_connection
# Remove circular import top-level imports
# from lib.models.author import Author
# from lib.models.magazine import Magazine

class Article:
    def __init__(self, id, title, author_id, magazine_id):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create(cls, title, author_id, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", (title, author_id, magazine_id))
        conn.commit()
        return cls(cursor.lastrowid, title, author_id, magazine_id)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM articles WHERE id = ?", (id,)).fetchone()
        if row:
            return cls.from_row(row)
        return None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM articles WHERE title = ?", (title,)).fetchone()
        if row:
            return cls.from_row(row)
        return None

    def author(self):
        from lib.models.author import Author  # import here to avoid circular import
        return Author.find_by_id(self.author_id)

    def magazine(self):
        from lib.models.magazine import Magazine  # import here
        return Magazine.find_by_id(self.magazine_id)

    @classmethod
    def from_row(cls, row):
        return cls(row["id"], row["title"], row["author_id"], row["magazine_id"])
