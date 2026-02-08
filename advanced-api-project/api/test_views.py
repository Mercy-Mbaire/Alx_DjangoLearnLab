from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book
from django.urls import reverse

class BookTests(APITestCase):
    def setUp(self):
        # Create User
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Create Data
        self.author = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")
        self.book1 = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)
        self.book2 = Book.objects.create(title="1984", publication_year=1949, author=self.author2)
        
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_authenticated(self):
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Book')

    def test_create_book_unauthenticated(self):
        self.client.logout()
        data = {'title': 'New Book', 'publication_year': 2023, 'author': self.author.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        data = {'title': 'Harry Potter Updated', 'publication_year': 1997, 'author': self.author.id}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter Updated')

    def test_delete_book_authenticated(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url, {'author': self.author.name}) # Filtering by name? No, field is 'author' which is ID or we need to check how filter works.
        # Check settings: filterset_fields = ['title', 'author', 'publication_year']
        # 'author' field on model is FK. Default exact match usually expects ID.
        # Let's try with ID first.
        response = self.client.get(self.list_url, {'author': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')

    def test_search_books(self):
        # search_fields = ['title', 'author__name']
        response = self.client.get(self.list_url, {'search': 'Orwell'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
        
        response = self.client.get(self.list_url, {'search': 'Harry'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')

    def test_order_books(self):
        # ordering_fields = ['title', 'publication_year']
        # Default is title. 1984 comes before Harry Potter.
        response = self.client.get(self.list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], '1984')
        
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], '1984') # 1949 < 1997

        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')
