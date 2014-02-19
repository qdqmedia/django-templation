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

DUMP_STACK_TRACE = getattr(settings, 'TEMPLATION_DUMP_STACK_TRACE', False)
DUMP_EXCEPTIONS = getattr(settings, 'TEMPLATION_DUMP_EXCEPTION', (
    'TemplateDoesNotExist',
    'TemplateSyntaxError',
))

SECRET_KEY = getattr(settings, 'TEMPLATION_SECRET_KEY', settings.SECRET_KEY)

VALIDATED_IDS_CACHE_TIME = getattr(settings, 'TEMPLATION_VALIDATED_IDS_CACHE_TIME', 60)

SANDBOX_TEMPLATES = getattr(settings, 'TEMPLATION_SANDBOX_TEMPLATES', False)

# Default tag whitelist
DEFAULT_WHITELIST_TAGS = [
    'comment', 'csrf_token', 'cycle', 'filter', 'firstof', 'for', 'if',
    'ifchanged', 'now', 'regroup', 'spaceless', 'templatetag', 'url',
    'widthratio', 'with', 'extends', 'include', 'block'
]
WHITELIST_TAGS = getattr(settings, 'TEMPLATION_WHITELIST_TAGS', DEFAULT_WHITELIST_TAGS)

# Default filter whitelist
DEFAULT_WHITELIST_FILTERS = [
    'add', 'addslashes', 'capfirst', 'center', 'cut', 'date', 'default',
    'default_if_none', 'dictsort', 'dictsortreversed', 'divisibleby', 'escape',
    'escapejs', 'filesizeformat', 'first', 'fix_ampersands', 'floatformat',
    'force_escape', 'get_digit', 'iriencode', 'join', 'last', 'length', 'length_is',
    'linebreaks', 'linebreaksbr', 'linenumbers', 'ljust', 'lower', 'make_list',
    'phone2numeric', 'pluralize', 'pprint', 'random', 'removetags', 'rjust', 'safe',
    'safeseq', 'slice', 'slugify', 'stringformat', 'striptags', 'time', 'timesince',
    'timeuntil', 'title', 'truncatewords', 'truncatewords_html', 'unordered_list',
    'upper', 'urlencode', 'urlize', 'urlizetrunc', 'wordcount', 'wordwrap', 'yesno'
]
WHITELIST_FILTERS = getattr(settings, 'TEMPLATION_WHITELIST_FILTERS', DEFAULT_WHITELIST_FILTERS)

# Custom libraries to add to builtins
DEFAULT_EXTRA_LIBRARIES = [
    'templation.templatetags.templation_tags',
]
EXTRA_LIBRARIES = getattr(settings, 'TEMPLATION_EXTRA_LIBRARIES', DEFAULT_EXTRA_LIBRARIES)
