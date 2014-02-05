"""
Manager to handle buitlin template tags and filters.
"""
from django.conf import settings
from django.template import base


BUILTIN_LIBRARYS = getattr(settings, 'TEMPLATION_BUILTIN_LIBRARYS', {
    'django.template.defaulttags': {},
    'django.template.defaultfilters': {},
    'django.template.loader_tags': {},
})

base.builtins = []

for k, v in BUILTIN_LIBRARYS.items():
    base.add_to_builtins(k)
    if 'exclude' in v:
        for kind, list in v['exclude'].items():
            for i in list:
                del getattr(base.builtins[-1], kind)[i]
