from lib.models.author import Author
from lib.models.magazine import Magazine

def seed_data():
    # Create authors
    maya = Author.create("Maya Angelou")
    george = Author.create("George Orwell")
    jane = Author.create("Jane Austen")
    
    # Create magazines
    time = Magazine.create("Time", "News")
    science = Magazine.create("Science Today", "Science")
    lit = Magazine.create("Literature Monthly", "Literature")

    # Create articles
    maya.add_article(time, "Freedom and You")
    maya.add_article(science, "Physics of Poetry")
    maya.add_article(lit, "Poetic Justice")
    
    george.add_article(time, "Big Brother Lives")
    george.add_article(science, "Politics and Science")
    
    jane.add_article(lit, "Romance and Reality")
