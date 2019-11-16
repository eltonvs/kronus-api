from clock_in_out.users.models import BaseUser


def create_user(*, full_name: str, email: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(email, password, full_name)
