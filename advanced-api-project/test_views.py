import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from api.models import Author, Book

def run_tests():
    print("Starting View Verification...")
    
    # Clean up
    User.objects.all().delete()
    Author.objects.all().delete()
    Book.objects.all().delete()

    client = APIClient()

    # Create User
    user = User.objects.create_user(username='testuser', password='password')
    
    # Create Author
    author = Author.objects.create(name="J.K. Rowling")
    
    # Create Book
    book = Book.objects.create(title="Harry Potter", publication_year=1997, author=author)

    # 1. Test List View (Public)
    response = client.get('/api/books/')
    if response.status_code == status.HTTP_200_OK:
        print("✅ List View (Public): PASSED")
    else:
        print(f"❌ List View (Public): FAILED ({response.status_code})")

    # 2. Test Detail View (Public)
    response = client.get(f'/api/books/{book.id}/')
    if response.status_code == status.HTTP_200_OK:
        print("✅ Detail View (Public): PASSED")
    else:
        print(f"❌ Detail View (Public): FAILED ({response.status_code})")

    # 3. Test Create View (Unauthenticated)
    data = {'title': 'New Book', 'publication_year': 2023, 'author': author.id}
    response = client.post('/api/books/create/', data)
    if response.status_code == status.HTTP_401_UNAUTHORIZED: # Or 403 depending on config
         print("✅ Create View (Unauthenticated): PASSED (Access Denied)")
    else:
         print(f"❌ Create View (Unauthenticated): FAILED (Expected 401/403, got {response.status_code})")

    # 4. Test Create View (Authenticated)
    client.force_authenticate(user=user)
    response = client.post('/api/books/create/', data)
    if response.status_code == status.HTTP_201_CREATED:
        print("✅ Create View (Authenticated): PASSED")
        new_book_id = response.data['id']
    else:
        print(f"❌ Create View (Authenticated): FAILED ({response.status_code})")
        if hasattr(response, 'data'):
            print(response.data)
        else:
            print(response.content)
        return

    # 5. Test Update View (Authenticated)
    update_data = {'title': 'Updated Title', 'publication_year': 2023, 'author': author.id}
    response = client.put(f'/api/books/update/{new_book_id}/', update_data)
    if response.status_code == status.HTTP_200_OK:
        print("✅ Update View (Authenticated): PASSED")
    else:
        print(f"❌ Update View (Authenticated): FAILED ({response.status_code})")
        print(response.data)

    # 6. Test Delete View (Authenticated)
    response = client.delete(f'/api/books/delete/{new_book_id}/')
    if response.status_code == status.HTTP_204_NO_CONTENT:
        print("✅ Delete View (Authenticated): PASSED")
    else:
         print(f"❌ Delete View (Authenticated): FAILED ({response.status_code})")

if __name__ == "__main__":
    run_tests()
