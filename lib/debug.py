from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

print("🔍 Debug Mode")

author = Author(name="Debug Dan")
author.save()
print("Saved:", author.id, author.name)

mag = Magazine(name="Science Now", category="Science")
mag.save()
print("Saved:", mag.id, mag.name)

article = Article(title="Quantum Realm", author_id=author.id, magazine_id=mag.id)
article.save()
print("Saved:", article.id, article.title)
