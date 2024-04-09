from django.test import TestCase, Client
from django.urls import reverse
# from django.contrib.auth.models import User
from accounts.models import CustomUser
class BooksTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

    def test_books(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        # Test title
        self.assertContains(response, '<title>My Django App</title>', html=True)

        # Test navigation links
        self.assertContains(response, '<a href="' + reverse('index') + '">Home</a>', html=True)
        self.assertContains(response, '<a href="' + reverse('accounts:login') + '">Log In</a>', html=True)
        self.assertContains(response, '<a href="' + reverse('accounts:signup') + '">Sign Up</a>', html=True)

        # Test guest message
        self.assertContains(response, 'Hello, guest! Please <a href="' + reverse('accounts:login') + '">log in</a>.', html=True)

        # Login the user
        self.client.login(username='testuser', password='testpassword')

        # Test navigation links and message after login
        response = self.client.get(reverse('index'))
        self.assertContains(response, '<a href="' + reverse('accounts:logout') + '">Logout</a>', html=True)
        self.assertContains(response, 'Hello, testuser!', html=True)
