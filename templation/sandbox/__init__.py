"""
Manager to handle buitlin template tags and filters.
"""
from django.conf import settings
from django.template import base
from ..utils import will_override


EXCLUDED = getattr(settings, 'TEMPLATION_EXCLUDED', {
    'tags': {},
    'filters': {}
})


class FilterDict(object):
    _original = None
    _sandbox = None

    def __init__(self, original, excluded):
        self._original = original
        self._sandbox = dict([(k, v) for k, v in original.items() if k not in excluded])

    def __call__(self, *args, **kwargs):
        if will_override()[0]:
            return self._sandbox
        return self._original


def Parser__init__(self, tokens):
    self.tokens = tokens
    self.tags = FilterDict(base.Parser.tags, EXCLUDED['tags'])
    self.filters = FilterDict(base.Parser.filters, EXCLUDED['tags'])
    for lib in builtins:
        self.add_library(lib)

base.Parser.__init__ = Parser__init__