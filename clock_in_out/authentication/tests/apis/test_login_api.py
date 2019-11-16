from unittest.mock import patch

from django.test import Client
from faker import Factory
from rest_framework.reverse import reverse
from test_plus import TestCase

from clock_in_out.users.factories import BaseUserFactory

faker = Factory.create()
client = Client()


class LoginApiTest(TestCase):

    def setUp(self):
        self.test_email = faker.email()
        self.test_password = faker.password()
        self.user = BaseUserFactory(email=self.test_email)
        self.user.set_password(self.test_password)
        self.user.is_active = True
        self.user.save()

        self.login_url = reverse('login')

    def test_user_cannot_login_with_wrong_email(self):
        email = faker.email()
        data = {
            'email': email,
            'password': self.test_password,
        }

        response = client.post(self.login_url, data=data)

        self.assertEqual(response.status_code, 400)

    def test_user_cannot_login_with_wrong_password(self):
        password = faker.password()
        data = {
            'email': self.user.email,
            'password': password,
        }

        response = client.post(self.login_url, data=data)

        self.assertEqual(response.status_code, 400)

    def test_user_cannot_login_if_account_is_inactive(self):
        self.user.is_active = False
        self.user.save()

        data = {
            'email': self.user.email,
            'password': self.test_password,
        }

        response = client.post(self.login_url, data=data)

        self.assertEqual(response.status_code, 400)

    @patch('clock_in_out.authentication.apis.get_user_data')
    def test_user_can_login_when_account_is_active(self, mock_object):
        mock_object.return_value = {}

        data = {
            'email': self.user.email,
            'password': self.test_password,
        }

        response = self.post(self.login_url, data=data)

        self.assertTrue(mock_object.called)
        self.assertEqual(response.status_code, 200)
