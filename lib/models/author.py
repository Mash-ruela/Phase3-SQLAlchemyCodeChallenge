from lib.db.connection import get_connection
# Removed top-level imports of Article and Magazine to avoid circular import

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        conn.commit()
        return cls(cursor.lastrowid, name)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM authors WHERE id = ?", (id,)).fetchone()
        if row:
            return cls(row["id"], row["name"])
        return None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM authors WHERE name = ?", (name,)).fetchone()
        if row:
            return cls(row["id"], row["name"])
        return None

    def articles(self):
        from lib.models.article import Article  # import here to avoid circular import
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self.id,)).fetchall()
        return [Article.from_row(row) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine  # import here too
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,)).fetchall()
        return [Magazine.from_row(row) for row in rows]

    def add_article(self, magazine, title):
        from lib.models.article import Article
        return Article.create(title, self.id, magazine.id)

    def topic_areas(self):
        return list({m.category for m in self.magazines()})

    @classmethod
    def top_author(cls):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("""
            SELECT a.*, COUNT(ar.id) AS article_count FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """).fetchone()
        if row:
            return cls(row["id"], row["name"])
        return None
