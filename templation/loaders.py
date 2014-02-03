"""
Wrapper for loading templates from the filesystem.
"""

from threading import local
from django.template import loader

_thread_vars = local()


class TemplationLoader(loader.app_directories.Loader):
    def get_template_sources(self, template_name, template_dirs=None):
        """ Add the resource dir to the available dirs. """

        res = getattr(_thread_vars, 'resource_access', None)
        if res:
            template_dirs = (res.get_absolute_url(),) + (template_dirs or ())

        super(TemplationLoader, self).get_template_sources(template_name,
                                                           template_dirs)
