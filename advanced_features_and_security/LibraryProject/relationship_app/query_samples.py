import sys
import os
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    # Create Author
    author_name = "George Orwell"
    author, created = Author.objects.get_or_create(name=author_name)
    
    # Create Book
    book_title = "1984"
    book, created = Book.objects.get_or_create(title=book_title, author=author)
    
    # Create Library
    library_name = "City Library"
    library, created = Library.objects.get_or_create(name=library_name)
    library.books.add(book)
    
    # Create Librarian
    librarian_name = "John Doe"
    librarian, created = Librarian.objects.get_or_create(name=librarian_name, library=library)
    
    print(f"Sample data created: Author {author.name}, Book {book.title}, Library {library.name}, Librarian {librarian.name}")

def query_samples():
    # Query 1: Query all books by a specific author
    author_name = "George Orwell"
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)
    print(f"Books by {author_name}: {[book.title for book in books_by_author]}")

    # Query 2: List all books in a library
    library_name = "City Library"
    library = Library.objects.get(name=library_name)
    books_in_library = library.books.all()
    print(f"Books in {library_name}: {[book.title for book in books_in_library]}")

    # Query 3: Retrieve the librarian for a library
    librarian = Librarian.objects.get(library=library)
    print(f"Librarian for {library_name}: {librarian.name}")

if __name__ == "__main__":
    create_sample_data()
    query_samples()
