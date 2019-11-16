import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from clock_in_out.common.models import UpdatedAtCreatedAtModelMixin
from clock_in_out.users.managers import UserManager


class BaseUser(PermissionsMixin, AbstractBaseUser, UpdatedAtCreatedAtModelMixin):
    full_name = models.CharField(blank=True, max_length=255)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    secret_key = models.UUIDField(default=uuid.uuid4, unique=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.email}'

    def rotate_secret_key(self):
        self.secret_key = uuid.uuid4()
        self.save()
