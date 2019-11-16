from django.test import TestCase

from clock_in_out.authentication.services import logout
from clock_in_out.users.factories import BaseUserFactory


class LogoutTests(TestCase):

    def setUp(self):
        self.user = BaseUserFactory()

    def test_logout_rotates_user_secret_key(self):
        previous_key = self.user.secret_key

        logout(user=self.user)
        self.user.refresh_from_db()

        self.assertNotEqual(previous_key, self.user.secret_key)
