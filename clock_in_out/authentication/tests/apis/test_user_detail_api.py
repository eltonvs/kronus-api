from unittest.mock import patch

from django.test import Client
from faker import Factory
from rest_framework.reverse import reverse
from test_plus import TestCase

from clock_in_out.users.factories import BaseUserFactory

faker = Factory.create()
client = Client()


class UserDetailApiTest(TestCase):

    def setUp(self):
        self.test_email = faker.email()
        self.test_password = faker.password()
        self.user = BaseUserFactory(email=self.test_email)
        self.user.set_password(self.test_password)
        self.user.is_active = True
        self.user.save()

        self.login_url = reverse('login')
        self.user_detail_url = reverse('user-detail')
        self.data = {
            'email': self.test_email,
            'password': self.test_password,
        }

    @patch('clock_in_out.authentication.apis.get_user_data')
    def test_cannot_fetch_user_data_with_invalid_token(self, mock_object):
        mock_object.return_value = {}

        login_response = client.post(self.login_url, data=self.data)
        token = login_response.data['token']

        # that should invalidate all previously aquired tokens
        self.user.rotate_secret_key()

        response = client.get(self.user_detail_url, HTTP_AUTHORIZATION=f'JWT {token}')

        self.assertTrue(mock_object.called)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'].code, 'authentication_failed')

    @patch('clock_in_out.authentication.apis.get_user_data')
    def test_can_fetch_use_data_with_valid_token(self, mock_object):
        mock_object.return_value = {}

        login_response = client.post(self.login_url, data=self.data)
        token = login_response.data['token']

        response = client.get(self.user_detail_url, HTTP_AUTHORIZATION=f'JWT {token}')

        self.assertTrue(mock_object.called)
        self.assertEqual(response.status_code, 200)
