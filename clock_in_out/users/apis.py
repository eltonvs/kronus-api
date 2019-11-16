from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from clock_in_out.apis.mixins import ServiceExceptionHandlerMixin
from clock_in_out.users.services import create_user


class SignupApi(ServiceExceptionHandlerMixin, APIView):

    class Serializer(serializers.Serializer):
        full_name = serializers.CharField()
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        data = request.data
        serializer = self.Serializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = create_user(**serializer.validated_data)
        data = {
            'full_name': user.full_name,
            'email': user.email,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
