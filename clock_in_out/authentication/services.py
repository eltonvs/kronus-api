from django.db import transaction
from rest_framework import serializers

from clock_in_out.users.models import BaseUser


class _UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseUser
        fields = ('id', 'email', 'full_name')


def get_user_data(*, user: BaseUser) -> dict:
    return _UserSerializer(instance=user).data


@transaction.atomic
def logout(*, user: BaseUser) -> BaseUser:
    user.rotate_secret_key()
    return user
