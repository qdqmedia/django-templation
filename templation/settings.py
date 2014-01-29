from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.db.models import get_model


# WebDav settings
PROVIDER_NAME = getattr(settings, 'TEMPLATION_PROVIDER_NAME', 'templation')

try:
    DAV_ROOT = settings.TEMPLATION_DAV_ROOT
except AttributeError:
    raise ImproperlyConfigured('You need to set TEMPLATION_DAV_ROOT in settings.py')

try:
    RESOURCE_MODEL = settings.TEMPLATION_RESOURCE_MODEL
except AttributeError:
    raise ImproperlyConfigured('You have to define TEMPLATION_RESOURCE_MODEL ("yourapp.YourModel") in settings.py')


# Model Getters
get_resource_access_model = lambda: get_model(*getattr(settings, 'TEMPLATION_RESOURCE_ACCESS_MODEL', 'templation.ResourceAccess').split('.'))
get_resource_model = lambda: get_model(*RESOURCE_MODEL.split('.'))
