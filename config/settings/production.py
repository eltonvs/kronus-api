from .base import *  # noqa, pylint: disable=wildcard-import,unused-wildcard-import

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env('DJANGO_SECRET_KEY')  # noqa: F405

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list(  # noqa: F405
    'DJANGO_ALLOWED_HOSTS', default=['localhost', 'https://kronus-api.herokuapp.com/']
)
