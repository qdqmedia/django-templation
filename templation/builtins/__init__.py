"""
Manager to handle buitlin template tags and filters.
"""
from django.conf import settings
from django.template import base, TemplateSyntaxError
from ..locals import thread_locals


BUILTIN_LIBRARIES = getattr(settings, 'TEMPLATION_BUILTIN_LIBRARIES', {
    'django.template.defaultfilters': {},
    'django.template.defaulttags': {},
    'django.template.loader_tags': {},
})

base.builtins = []


class exclusion_filter(object):
    def __init__(self, function):
        self._decorated_function = function

    def __call__(self, *args, **kwargs):
        if thread_locals.resource:
            raise TemplateSyntaxError('{} is not a valid tag/filter to use in templation'.format(self._decorated_function.__name__))
        return self._decorated_function(*args, **kwargs)


for k, v in BUILTIN_LIBRARIES.items():
    base.add_to_builtins(k)
    if 'exclude' in v:
        for kind, list in v['exclude'].items():
            obj = getattr(base.builtins[-1], kind)
            for i in list:
                obj[i] = exclusion_filter(obj[i])
