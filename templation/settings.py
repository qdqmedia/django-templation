from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


PROVIDER_NAME = getattr(settings, 'TEMPLATION_PROVIDER_NAME', 'templation')

try:
    DAV_ROOT = settings.TEMPLATION_DAV_ROOT
except AttributeError:
    raise ImproperlyConfigured('You need to set TEMPLATION_DAV_ROOT in settings.py')

try:
    RESOURCE_MODEL = settings.TEMPLATION_RESOURCE_MODEL
except AttributeError:
    raise ImproperlyConfigured('You have to define TEMPLATION_RESOURCE_MODEL ("yourapp.YourModel") in settings.py')
