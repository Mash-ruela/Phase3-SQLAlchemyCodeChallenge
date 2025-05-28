from lib.models.author import Author

def test_author_save():
    a = Author(name="Tester")
    a.save()
    assert a.id is not None
