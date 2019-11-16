import jwt
from django.test import Client
from faker import Factory
from jwt.exceptions import InvalidSignatureError
from rest_framework.reverse import reverse
from test_plus import TestCase

from clock_in_out.users.factories import BaseUserFactory

faker = Factory.create()
client = Client()


class JWTSecretTest(TestCase):

    def setUp(self):
        self.test_email = faker.email()
        self.test_password = faker.password()
        self.user = BaseUserFactory(email=self.test_email)
        self.user.set_password(self.test_password)
        self.user.is_active = True
        self.user.save()

        self.initial_secret_key = self.user.secret_key
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user_detail_url = reverse('user-detail')
        self.data = {
            'email': self.user.email,
            'password': self.test_password,
        }

    def test_user_can_decode_only_own_tokens(self):
        response = self.post(self.login_url, data=self.data)
        token = response.data['token']

        user = BaseUserFactory()
        user.is_active = True
        pwd = faker.password()
        user.set_password(pwd)
        user.save()
        data = {
            'email': user.email,
            'password': pwd,
        }
        other_response = self.post(self.login_url, data=data)
        other_token = other_response.data['token']

        self.assertNotEqual(token, other_token)
        self.assertNotEqual(self.user.secret_key, user.secret_key)

        with self.assertRaises(InvalidSignatureError):
            jwt.decode(token, key=str(user.secret_key))

        with self.assertRaises(InvalidSignatureError):
            jwt.decode(other_token, key=str(self.user.secret_key))

        jwt_decoded = jwt.decode(token, key=str(self.user.secret_key))
        self.assertEqual(self.user.email, jwt_decoded['email'])

        other_jwt_decoded = jwt.decode(other_token, key=str(user.secret_key))
        self.assertEqual(user.email, other_jwt_decoded['email'])

    def test_user_can_access_restrict_urls_only_after_login(self):
        response = self.post(self.login_url, data=self.data)
        token = response.data['token']

        restrict_response = client.get(self.user_detail_url, HTTP_AUTHORIZATION=f'JWT {token}')

        self.assertEqual(restrict_response.status_code, 200)
        self.assertEqual(restrict_response.data['email'], self.user.email)

    def test_user_cannot_use_old_token_after_logout(self):
        response = self.post(self.login_url, data=self.data)
        token = response.data['token']

        client.post(self.logout_url, HTTP_AUTHORIZATION=f'JWT {token}')

        restrict_response = client.get(self.user_detail_url, HTTP_AUTHORIZATION=f'JWT {token}')

        self.assertEqual(restrict_response.status_code, 401)

    def test_user_gets_new_secret_key_after_logout(self):
        response = self.post(self.login_url, data=self.data)
        token = response.data['token']

        client.post(self.logout_url, HTTP_AUTHORIZATION=f'JWT {token}')

        self.user.refresh_from_db()

        self.assertNotEqual(self.initial_secret_key, self.user.secret_key)
