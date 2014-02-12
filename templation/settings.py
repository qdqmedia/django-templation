from __future__ import absolute_import
from importlib import import_module
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

# global switch to show templation dump_errors
DEBUG = getattr(settings, 'TEMPLATION_DEBUG',
                not bool(getattr(settings, 'DEBUG', True)))


def import_from_path(import_string):
    try:
        module, name = import_string.rsplit('.', 1)
        return getattr(import_module(module), name)
    except (AttributeError, ValueError):  # pragma no cover
        raise ImportError(import_string)

try:
    DAV_ROOT = settings.TEMPLATION_DAV_ROOT
except AttributeError:  # pragma no cover
    raise ImproperlyConfigured('You need to set TEMPLATION_DAV_ROOT in settings.py')

try:
    DAV_STATIC_URL = settings.TEMPLATION_DAV_STATIC_URL
except AttributeError:  # pragma no cover
    raise ImproperlyConfigured('You need to set TEMPLATION_DAV_STATIC_URL in settings.py')

try:
    RESOURCE_MODEL = settings.TEMPLATION_RESOURCE_MODEL
except AttributeError:  # pragma no cover
    raise ImproperlyConfigured('You have to define TEMPLATION_RESOURCE_MODEL = "yourapp.models.YourModel" in settings.py')

# WebDav settings
PROVIDER_NAME = getattr(settings, 'TEMPLATION_PROVIDER_NAME', 'templation')
BOILERPLATE_FOLDER = getattr(settings, 'TEMPLATION_BOILERPLATE_FOLDER', None)
BOILERPLATE_INITIALIZER = getattr(settings,
                                  'TEMPLATION_BOILERPLATE_INITIALIZER',
                                  'templation.models.copy_boilerplate_folder')

# Model Getters
get_resource_access_model = lambda: \
    import_from_path(getattr(settings, 'TEMPLATION_RESOURCE_ACCESS_MODEL',
                             'templation.models.ResourceAccess'))
get_resource_model = lambda: import_from_path(RESOURCE_MODEL)

DUMP_REPORT_STRATEGY = getattr(settings, 'TEMPLATION_DUMP_REPORT_STRATEGY',
                               'templation.middleware.dump_report_strategy')

DUMP_STACK_TRACE = getattr(settings, 'TEMPLATION_DUMP_STACK_TRACE', False)
DUMP_EXCEPTIONS = getattr(settings, 'TEMPLATION_DUMP_EXCEPTION', (
    'TemplateDoesNotExist',
    'TemplateSyntaxError',
))

VALIDATED_IDS_CACHE_TIME = getattr(settings, 'TEMPLATION_VALIDATED_IDS_CACHE_TIME', 60)
