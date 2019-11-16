from unittest.mock import patch

from django.test import Client
from faker import Factory
from rest_framework.reverse import reverse
from test_plus import TestCase

from clock_in_out.users.factories import BaseUserFactory

faker = Factory.create()
client = Client()


class LogoutApiTest(TestCase):

    def setUp(self):
        self.test_email = faker.email()
        self.test_password = faker.password()
        self.user = BaseUserFactory(email=self.test_email)
        self.user.set_password(self.test_password)
        self.user.is_active = True
        self.user.save()

        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.data = {
            'email': self.test_email,
            'password': self.test_password,
        }

    @patch('clock_in_out.authentication.apis.get_user_data')
    def test_logout_user_with_invalid_token(self, mock_object):
        mock_object.return_value = {}

        login_response = client.post(self.login_url, data=self.data)
        token = login_response.data['token']

        # that should invalidate all generated tokens until now
        self.user.rotate_secret_key()

        # try to perform api logout
        logout_response = client.post(self.logout_url, HTTP_AUTHORIZATION=f'JWT {token}')

        self.assertEqual(logout_response.status_code, 401)

    @patch('clock_in_out.authentication.apis.get_user_data')
    @patch('clock_in_out.authentication.apis.logout')
    def test_logout_user_with_valid_token(self, mock1, mock2):
        mock2.return_value = {}

        login_response = client.post(self.login_url, data=self.data)
        token = login_response.data['token']

        # try to perform api logout
        logout_response = client.post(self.logout_url, HTTP_AUTHORIZATION=f'JWT {token}')

        self.assertTrue(mock1.called)
        self.assertTrue(mock2.called)
        self.assertEqual(logout_response.status_code, 202)
