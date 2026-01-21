from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from django.urls import reverse
from django.test import Client

class RBACTests(TestCase):
    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_user(username='admin_user', password='password')
        self.librarian_user = User.objects.create_user(username='librarian_user', password='password')
        self.member_user = User.objects.create_user(username='member_user', password='password')


        # Assign roles
        from .models import UserProfile
        
        # Admin
        admin_profile = UserProfile.objects.get(user=self.admin_user)
        admin_profile.role = 'Admin'
        admin_profile.save()
        
        # Librarian
        librarian_profile = UserProfile.objects.get(user=self.librarian_user)
        librarian_profile.role = 'Librarian'
        librarian_profile.save()
        
        # Member
        member_profile = UserProfile.objects.get(user=self.member_user)
        member_profile.role = 'Member'
        member_profile.save()

        self.client = Client()

    def test_admin_view_access(self):
        self.assertTrue(self.client.login(username='admin_user', password='password'), "Login failed for admin_user")
        response = self.client.get(reverse('admin_view'))
        self.assertEqual(response.status_code, 200)

        self.client.login(username='librarian_user', password='password')
        response = self.client.get(reverse('admin_view'))
        self.assertNotEqual(response.status_code, 200) # Should redirect or forbidden

    def test_librarian_view_access(self):
        self.client.login(username='librarian_user', password='password')
        response = self.client.get(reverse('librarian_view'))
        self.assertEqual(response.status_code, 200)

        self.client.login(username='member_user', password='password')
        response = self.client.get(reverse('librarian_view'))
        self.assertNotEqual(response.status_code, 200)

    def test_member_view_access(self):
        self.client.login(username='member_user', password='password')
        response = self.client.get(reverse('member_view'))
        self.assertEqual(response.status_code, 200)

        self.client.login(username='admin_user', password='password')
        response = self.client.get(reverse('member_view'))
        self.assertNotEqual(response.status_code, 200)
