from rest_framework import serializers, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from clock_in_out.apis.mixins import ServiceExceptionHandlerMixin
from clock_in_out.authentication.permissions import JSONWebTokenAuthenticationMixin
from clock_in_out.clock.models import ClockEntry
from clock_in_out.clock.services import create_clock_in, create_clock_out, update_clock_entry


class ClockInApi(JSONWebTokenAuthenticationMixin, ServiceExceptionHandlerMixin, APIView):

    class Serializer(serializers.Serializer):
        time = serializers.DateTimeField()

    def post(self, request):
        data = request.data
        serializer = self.Serializer(data=data)
        serializer.is_valid(raise_exception=True)

        clock_entry = create_clock_in(**{**serializer.validated_data, 'user': self.request.user})
        data = {
            'id': clock_entry.id,
            'time': clock_entry.time,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


class ClockOutApi(JSONWebTokenAuthenticationMixin, ServiceExceptionHandlerMixin, APIView):

    class Serializer(serializers.Serializer):
        time = serializers.DateTimeField()
        clock_in = serializers.IntegerField()

    def post(self, request):
        data = request.data
        serializer = self.Serializer(data=data)
        serializer.is_valid(raise_exception=True)

        clock_entry = create_clock_out(**{**serializer.validated_data, 'user': self.request.user})
        data = {
            'id': clock_entry.id,
            'time': clock_entry.time,
            'clock_in': clock_entry.clock_in.id,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)


class ClockLogApi(JSONWebTokenAuthenticationMixin, ServiceExceptionHandlerMixin, ListAPIView):

    class Serializer(serializers.ModelSerializer):

        class Meta:
            model = ClockEntry
            fields = (
                'id',
                'time',
                'clock_in',
                'clock_out',
            )

    serializer_class = Serializer

    def get_queryset(self):
        user = self.request.user

        return ClockEntry.objects.filter(user=user).order_by('time')


class ChangeClockEntryApi(JSONWebTokenAuthenticationMixin, ServiceExceptionHandlerMixin, APIView):

    class ClockEntrySerializer(serializers.ModelSerializer):

        class Meta:
            model = ClockEntry
            fields = (
                'id',
                'time',
                'clock_in',
                'clock_out',
            )

    class Serializer(serializers.Serializer):
        time = serializers.DateTimeField()
        out_pk = serializers.IntegerField(required=False, default=None, allow_null=True)
        out_time = serializers.DateTimeField(required=False, default=None, allow_null=True)

    def delete(self, request, pk):
        user = request.user
        clock_entry = ClockEntry.objects.get(user=user, pk=pk)
        clock_entry.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        user = request.user
        data = request.data
        serializer = self.Serializer(data=data)
        serializer.is_valid(raise_exception=True)

        clock_in, clock_out = update_clock_entry(**{**serializer.validated_data, 'user': user, 'pk': pk})

        data = {
            'clock_in': self.ClockEntrySerializer(clock_in).data,
            'clock_out': clock_out and self.ClockEntrySerializer(clock_out).data,
        }
        return Response(data=data, status=status.HTTP_200_OK)
