from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profile_app.models import Profile


# Create your tests here.
class CreateOfferViewTest(APITestCase):
    def setUp(self):
        self.customerUser = User.objects.create_user(username='customer', password='')
        self.businessUser = User.objects.create_user(username='business', password='')
        Profile.objects.create(user=self.customerUser, type='customer')
        Profile.objects.create(user=self.businessUser, type='business')

        self.data = {
            'title': 'title',
            'description': 'description',
            'details': [
                {
                    'title': 'basic',
                    'revisions': 2,
                    'delivery_time_in_days': 5,
                    'price': 100,
                    'features': [
                        "Feature A",
                        "Feature B",
                    ],
                    "offer_type": "basic"
                },
                {
                    'title': 'standard',
                    'revisions': 2,
                    'delivery_time_in_days': 5,
                    'price': 100,
                    'features': [
                        "Feature A",
                        "Feature B",
                    ],
                    "offer_type": "standard"
                },
                {
                    'title': 'premium',
                    'revisions': 2,
                    'delivery_time_in_days': 5,
                    'price': 100,
                    'features': [
                        "Feature A",
                        "Feature B",
                    ],
                    "offer_type": "premium"
                }
            ]
        }

    def test_post(self):
        token, _ = Token.objects.get_or_create(user=self.businessUser)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.post('/api/offers/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_detail_issue(self):
        token, _ = Token.objects.get_or_create(user=self.businessUser)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        self.data['details'].pop(2)
        response = self.client.post('/api/offers/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_failed_as_customer(self):
        token, _ = Token.objects.get_or_create(user=self.customerUser)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.client.post('/api/offers/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated(self):
        response = self.client.post('/api/offers/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)