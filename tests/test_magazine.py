import pytest
from lib.db.connection import get_connection
from lib.db.seed import seed_data
from lib.models.magazine import Magazine

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    conn = get_connection()
    with open("lib/db/schema.sql") as f:
        conn.executescript(f.read())
    seed_data()

def test_find_by_category():
    mags = Magazine.find_by_category("News")
    assert any(mag.name == "Time" for mag in mags)

def test_contributors_and_article_titles():
    mag = Magazine.find_by_id(1)  # Time
    contributors = mag.contributors()
    titles = mag.article_titles()
    assert len(contributors) > 0
    assert len(titles) > 0

def test_with_multiple_authors():
    mags = Magazine.with_multiple_authors()
    assert any(mag.name == "Time" for mag in mags)
