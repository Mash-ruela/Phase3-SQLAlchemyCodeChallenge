import pytest
from lib.db.connection import get_connection
from lib.db.seed import seed_data
from lib.models.article import Article

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    conn = get_connection()
    with open("lib/db/schema.sql") as f:
        conn.executescript(f.read())
    seed_data()

def test_find_by_title():
    article = Article.find_by_title("Freedom and You")
    assert article is not None
    assert article.title == "Freedom and You"

def test_create_article():
    article = Article.create("New Article", 1, 1)
    assert article.id is not None
    assert article.title == "New Article"
