from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def __create_user(self, email, full_name='', password=None, is_staff=False, is_active=True, is_superuser=False):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(
            email=email, full_name=full_name, is_staff=is_staff, is_active=is_active, is_superuser=is_superuser
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)

        return user

    def create_user(self, email, password, full_name=''):
        return self.__create_user(email, full_name, password, is_staff=False, is_active=True, is_superuser=False)

    def create_superuser(self, email, password, full_name=''):
        return self.__create_user(email, full_name, password, is_staff=True, is_active=True, is_superuser=True)

    def create(self, **kwargs):
        return self.create_user(**kwargs)
