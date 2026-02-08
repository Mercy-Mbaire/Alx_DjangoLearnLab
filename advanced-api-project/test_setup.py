import os
import django
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

def run_test():
    print("Starting verification...")
    # Clean up previous data
    Author.objects.all().delete()
    Book.objects.all().delete()

    # 1. Create Author
    author = Author.objects.create(name="George Orwell")
    print(f"Created Author: {author.name}")

    # 2. Create Book linked to Author
    book = Book.objects.create(title="1984", publication_year=1949, author=author)
    print(f"Created Book: {book.title} ({book.publication_year})")

    # 3. Test Validation (Future Year)
    print("\nTesting BookSerializer Validation:")
    future_year = datetime.now().year + 1
    # Note: For ModelSerializer, we pass the author primary key for writing if checking validation on creation
    # But BookSerializer default handles author as PK or we might need to adjust if we wanted nested write (which we didn't implement)
    # The default ModelSerializer for 'author' field expects a PK.
    data = {'title': 'Future Book', 'publication_year': future_year, 'author': author.id}
    serializer = BookSerializer(data=data)
    if serializer.is_valid():
        print("❌ Validation FAILED: Future year accepted.")
    else:
        print(f"✅ Validation PASSED: Future year rejected.")
        print(f"   Errors: {serializer.errors}")

    # 4. Test Valid Creation via Serializer
    data_valid = {'title': 'Animal Farm', 'publication_year': 1945, 'author': author.id}
    serializer_valid = BookSerializer(data=data_valid)
    if serializer_valid.is_valid():
        book2 = serializer_valid.save()
        print(f"✅ Valid Book Created via Serializer: {book2.title}")
    else:
        print(f"❌ Valid Creation FAILED. Errors: {serializer_valid.errors}")

    # 5. Test Nested Serialization (Author -> Books)
    print("\nTesting AuthorSerializer (Nested):")
    # Refresh author to get related books
    author.refresh_from_db()
    author_serializer = AuthorSerializer(author)
    serialized_data = author_serializer.data
    import json
    print(json.dumps(serialized_data, indent=2))
    
    books_data = serialized_data.get('books', [])
    if len(books_data) >= 2:
         print(f"✅ Nested serialization PASSED: Found {len(books_data)} books for author.")
    else:
         print(f"❌ Nested serialization FAILED: Found {len(books_data)} books (expected >= 2).")

if __name__ == "__main__":
    run_test()
