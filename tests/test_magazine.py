from lib.models.magazine import Magazine

def test_magazine_save():
    m = Magazine(name="TestMag", category="News")
    m.save()
    assert m.id is not None
