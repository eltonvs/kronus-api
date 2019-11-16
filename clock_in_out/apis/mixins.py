from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import exceptions as rest_exceptions

from clock_in_out.apis.utils import get_error_message


class ServiceExceptionHandlerMixin:
    '''Mixin to convert django and python exceptions into REST exceptions'''
    expected_exceptions = {
        # Python errors
        ValueError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied,
        # Django errors
        ValidationError: rest_exceptions.ValidationError,
        PermissionDenied: rest_exceptions.PermissionDenied,
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)
