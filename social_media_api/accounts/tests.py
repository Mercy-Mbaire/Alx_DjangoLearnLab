from django.test import TestCase
from .models import Post

class PostModelTest(TestCase):

    def setUp(self):
        self.post = Post.objects.create(
            title="Test Title",
            content="Test Content"
        )

    def test_post_created(self):
        self.assertEqual(self.post.title, "Test Title")
