from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def run_sample_queries():
    print("All authors:")
    for name in ["Maya Angelou", "George Orwell", "Jane Austen"]:
        author = Author.find_by_name(name)
        if author:
            print(f"- {author.name} writes {len(author.articles())} articles.")
    
    print("\nMagazines with multiple authors:")
    for mag in Magazine.with_multiple_authors():
        print(f"- {mag.name} ({mag.category})")
    
    print("\nTop author:")
    top = Author.top_author()
    print(f"{top.name} with most articles.")

if __name__ == "__main__":
    run_sample_queries()
