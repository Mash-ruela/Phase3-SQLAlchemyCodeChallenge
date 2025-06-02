from lib.db.connection import get_connection
# Removed top-level imports of Article and Author to avoid circular import

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @classmethod
    def create(cls, name, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
        conn.commit()
        return cls(cursor.lastrowid, name, category)

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,)).fetchone()
        if row:
            return cls.from_row(row)
        return None

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,)).fetchall()
        return [cls.from_row(row) for row in rows]

    def articles(self):
        from lib.models.article import Article  # import here
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,)).fetchall()
        return [Article.from_row(row) for row in rows]

    def contributors(self):
        from lib.models.author import Author  # import here
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT DISTINCT au.* FROM authors au
            JOIN articles ar ON ar.author_id = au.id
            WHERE ar.magazine_id = ?
        """, (self.id,)).fetchall()
        return [Author(row["id"], row["name"]) for row in rows]

    def article_titles(self):
        return [article.title for article in self.articles()]

    def contributing_authors(self):
        from lib.models.author import Author  # import here
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT a.*, COUNT(ar.id) AS total FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING total > 2
        """, (self.id,)).fetchall()
        return [Author(row["id"], row["name"]) for row in rows]

    @classmethod
    def with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            GROUP BY m.id
            HAVING COUNT(DISTINCT a.author_id) >= 2
        """).fetchall()
        return [cls.from_row(row) for row in rows]

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("""
            SELECT m.name, COUNT(a.id) AS article_count
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
        """).fetchall()
        return {row["name"]: row["article_count"] for row in rows}

    @classmethod
    def from_row(cls, row):
        return cls(row["id"], row["name"], row["category"])
