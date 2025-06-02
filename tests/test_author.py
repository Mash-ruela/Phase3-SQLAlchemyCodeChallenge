import pytest
from lib.db.connection import get_connection
from lib.db.seed import seed_data
from lib.models.author import Author

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    conn = get_connection()
    with open("lib/db/schema.sql") as f:
        conn.executescript(f.read())
    seed_data()

def test_find_by_name():
    author = Author.find_by_name("Maya Angelou")
    assert author is not None
    assert author.name == "Maya Angelou"

def test_articles_and_magazines():
    author = Author.find_by_name("Maya Angelou")
    articles = author.articles()
    magazines = author.magazines()
    assert len(articles) > 0
    assert len(magazines) > 0

def test_top_author():
    top = Author.top_author()
    assert top.name == "Maya Angelou"
