from django.core.exceptions import ValidationError
from faker import Factory
from test_plus import TestCase

from ..models import BaseUser

faker = Factory.create()


class BaseUserTests(TestCase):

    def setUp(self):
        self.email = faker.email()
        self.full_name = faker.name()
        self.test_password = faker.password()

    def test_create_user_creates_single_user(self):
        user_count = BaseUser.objects.count()
        BaseUser.objects.create_user(email=self.email, full_name=self.full_name, password=self.test_password)
        self.assertEqual(user_count + 1, BaseUser.objects.count())

    def test_create_user_raises_validation_error_when_email_invalid(self):
        with self.assertRaises(ValidationError):
            BaseUser.objects.create_user(email='invalid email', full_name=self.full_name, password=self.test_password)

    def test_create_user_raises_validation_error_when_user_already_exists(self):
        BaseUser.objects.create(email=self.email, full_name=self.full_name, password=self.test_password)
        with self.assertRaises(ValidationError):
            BaseUser.objects.create_user(email=self.email, full_name=self.full_name, password=self.test_password)

    def test_create_user_raises_value_error_when_no_email_is_provided(self):
        with self.assertRaises(ValueError):
            BaseUser.objects.create_user(email=None, full_name=self.full_name, password=self.test_password)
