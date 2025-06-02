from search_db_conn import get_connection
from .article import Article
from .author import Author

class Magazine:
    def __init__(self, id=None, name="", category=""):
        self.id = id
        self.name = name
        self.category = category

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE magazines SET name=?, category=? WHERE id=?",
                           (self.name, self.category, self.id))
        else:
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)",
                           (self.name, self.category))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(id=row[0], name=row[1]) for row in rows]

    def article_titles(self):
        articles = Article.find_by_magazine_id(self.id)
        return [a.title for a in articles]

    def contributing_authors(self):
        authors = self.contributors()
        return [a for a in authors if len(a.articles()) > 2]

    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM magazines WHERE category=?", (category,)).fetchone()
        conn.close()
        return cls(id=row[0], name=row[1], category=row[2]) if row else None

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM magazines WHERE name=?", (name,)).fetchone()
        conn.close()
        return cls(id=row[0], name=row[1], category=row[2]) if row else None

    @classmethod
    def with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazine_id FROM articles
            GROUP BY magazine_id, author_id
        """)
        data = cursor.fetchall()

        from collections import Counter
        counts = Counter([row[0] for row in data])
        result_ids = [mid for mid, count in counts.items() if count > 1]
        return [cls.find_by_id(mid) for mid in result_ids]

    @classmethod
    def article_counts(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id, m.name, m.category, COUNT(a.id) as article_count
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
        """)
        rows = cursor.fetchall()
        conn.close()
        return [{"id": row[0], "name": row[1], "category": row[2], "article_count": row[3]} for row in rows]

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM magazines WHERE id=?", (id,)).fetchone()
        conn.close()
        return cls(id=row[0], name=row[1], category=row[2]) if row else None
