"""
Wrapper for loading templates from the filesystem.
"""

from __future__ import absolute_import
from django.template.loaders.app_directories import Loader
from .settings import get_resource_access_model
from .utils import will_override


class TemplationLoader(Loader):
    def __init__(self):
        self._access = get_resource_access_model()

    def get_template_sources(self, template_name, template_dirs=None):
        """ Add the resource dir to the available dirs. """
        override, resource_access = will_override()
        if override:
            path = resource_access.get_path('templates')
            template_dirs = (path,) + (template_dirs or ())

        return super(TemplationLoader, self).get_template_sources(template_name,
                                                                  template_dirs)
