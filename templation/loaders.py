"""
Wrapper for loading templates from the filesystem.
"""

from django.template.loaders.app_directories import Loader
from .middleware import global_thread_vars


class TemplationLoader(Loader):
    def get_template_sources(self, template_name, template_dirs=None):
        """ Add the resource dir to the available dirs. """
        res = getattr(global_thread_vars, 'resource_access', None)
        if res:
            template_dirs = (res.get_absolute_url(),) + (template_dirs or ())

            super(TemplationLoader, self).get_template_sources(template_name,
                                                               template_dirs)
        return []
