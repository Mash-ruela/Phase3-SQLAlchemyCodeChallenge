from search_db_conn import get_connection

class Author:
    def __init__(self, id=None, name=""):
        self.id = id
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE authors SET name=? WHERE id=?", (self.name, self.id))
        else:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def add_article(self, magazine, title):
        from .article import Article
        Article(title=title, author_id=self.id, magazine_id=magazine.id).save()

    def articles(self):
        from .article import Article
        return Article.find_by_author_id(self.id)

    def magazines(self):
        from .magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(id=row[0], name=row[1], category=row[2]) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM authors WHERE name=?", (name,)).fetchone()
        conn.close()
        return cls(id=row[0], name=row[1]) if row else None

    @classmethod
    def top_author(cls):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("""
            SELECT author_id, COUNT(*) AS count FROM articles
            GROUP BY author_id ORDER BY count DESC LIMIT 1
        """).fetchone()
        conn.close()
        if row:
            return Author.find_by_id(row[0])
        return None

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM authors WHERE id=?", (id,)).fetchone()
        conn.close()
        return cls(id=row[0], name=row[1]) if row else None
