from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import LoginForm, SignupForm

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

class TestSignup(BaseTestCase):
    def test_signup(self):
        user_data = {
            'email': 'testuser@test.com',
            'username': 'testuser2',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

        response = self.client.post(reverse('accounts:signup'), user_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check if the user was created
        self.assertTrue(get_user_model().objects.filter(username='testuser2').exists())
        # Check if the user was logged in after signing up
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertTrue(response.context['user'].username, 'testuser2')

    def test_signup_invalid(self):
        user_data = {
            'email': 'testuser@test.com',
            'username': 'testuser2',
            'password1': 'testpassword',
            'password2': 'differentpassword'
        }

        response = self.client.post(reverse('accounts:signup'), user_data)
        self.assertEqual(response.status_code, 200)
        
        form = response.context['form']
        self.assertFormError(form, 'password2', 'The two password fields didn’t match.')

class TestLogout(BaseTestCase):
    def test_logout(self):
        # Login the user
        self.client.login(username='testuser', password='testpassword')

        # Check if the user is logged in
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello, testuser!', html=True)

        # Logout the user
        logout_url = reverse('accounts:logout')
        self.client.get(logout_url)

        # Check if the user is logged out
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello, guest! Please <a href="' + reverse('accounts:login') + '">log in</a>.', html=True)

class TestLogin(BaseTestCase):
    def test_login(self):
        # Check if the user is not logged in
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello, guest! Please <a href="' + reverse('accounts:login') + '">log in</a>.', html=True)

        # Login the user
        login_url = reverse('accounts:login')
        response = self.client.post(login_url, {'username': 'testuser', 'password': 'testpassword'}, follow=True)

        # Check if the user is logged in
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello, testuser!', html=True)

    def test_login_invalid(self):
        # Check if the user is not logged in
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello, guest! Please <a href="' + reverse('accounts:login') + '">log in</a>.', html=True)

        # Try to login with invalid credentials
        login_url = reverse('accounts:login')
        response = self.client.post(login_url, {'username': 'testuser', 'password': 'wrongpassword'})

        # Check if the user is not logged in
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be case-sensitive.', html=True)
