from .base import *  # noqa, pylint: disable=wildcard-import,unused-wildcard-import

DEBUG = env.bool('DJANGO_DEBUG', default=True)  # noqa: F405

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa: F405

SECRET_KEY = env('DJANGO_SECRET_KEY', default='bjqrep7)%=m2_!3h-b3uv1ufysmh5gqtlk3*==id(brl58!b_')  # noqa: F405
