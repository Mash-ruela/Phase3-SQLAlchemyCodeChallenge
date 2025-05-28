from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

def test_article_save():
    a = Author(name="Test A")
    a.save()
    m = Magazine(name="Test M", category="Test")
    m.save()
    art = Article(title="Test Title", author_id=a.id, magazine_id=m.id)
    art.save()
    assert art.id is not None
