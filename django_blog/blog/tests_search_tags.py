from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class BlogSearchTagsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post1 = Post.objects.create(
            title='Django Guide',
            content='Learn Django models and views.',
            author=self.user
        )
        self.post1.tags.add('django', 'python')
        
        self.post2 = Post.objects.create(
            title='Flask vs FastAPI',
            content='Comparing microframeworks.',
            author=self.user
        )
        self.post2.tags.add('fastapi', 'python')

    def test_search_by_title(self):
        response = self.client.get(reverse('search-results') + '?q=Django')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Guide')
        self.assertNotContains(response, 'Flask vs FastAPI')

    def test_search_by_content(self):
        response = self.client.get(reverse('search-results') + '?q=models')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Guide')

    def test_search_by_tags(self):
        response = self.client.get(reverse('search-results') + '?q=fastapi')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Flask vs FastAPI')
        self.assertNotContains(response, 'Django Guide')

    def test_tag_filtered_view(self):
        response = self.client.get(reverse('post-by-tag', kwargs={'tag_name': 'python'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django Guide')
        self.assertContains(response, 'Flask vs FastAPI')

        response = self.client.get(reverse('post-by-tag', kwargs={'tag_name': 'django'}))
        self.assertContains(response, 'Django Guide')
        self.assertNotContains(response, 'Flask vs FastAPI')
