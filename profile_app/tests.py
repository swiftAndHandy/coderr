from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from profile_app.models import Profile


# Create your tests here.
class ProfileDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@backend.org', password='test')
        self.profile = Profile.objects.create(user=self.user, type='customer')

    def test_get_unauthenticated_returns_401(self):
        response = self.client.get(f'/api/profile/{self.profile.user_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)