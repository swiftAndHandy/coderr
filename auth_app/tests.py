from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase

from profile_app.models import Profile


# Create your tests here.
class RegistrationPostTest(APITestCase):
    def test_registration_success(self):
        data = {
            'username': 'testuser',
            'email': 'test@test.de',
            'password': 'test',
            'repeated_password': 'test',
            'type': 'customer'
        }

        response = self.client.post('/api/registration/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_password_missmatch(self):
        data = {
            'username': 'testuser',
            'email': 'test@test.de',
            'password': 'test',
            'repeated_password': 'test123',
            'type': 'customer'
        }

        response = self.client.post('/api/registration/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_type(self):
        data = {
            'username': 'testuser',
            'email': 'test@test.de',
            'password': 'test',
            'repeated_password': 'test',
            'type': 'zebra'
        }

        response = self.client.post('/api/registration/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_already_exists(self):
        data = {
            'username': 'testuser',
            'email': 'test@test.de',
            'password': 'test',
            'repeated_password': 'test',
            'type': 'customer'
        }

        self.client.post('/api/registration/', data)
        response = self.client.post('/api/registration/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class LoginPostTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@backend.org', password='test')
        self.profile = Profile.objects.create(user=self.user, type='customer')

    def test_login_success(self):
        data = {
            'username': 'testuser',
            'password': 'test'
        }

        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
