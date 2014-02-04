"""
Wrapper for loading templates from the filesystem.
"""

from django.template.loaders.app_directories import Loader
from .locals import thread_locals
from .settings import get_resource_access_model


class TemplationLoader(Loader):
    def __init__(self):
        self._access = get_resource_access_model()

    def get_template_sources(self, template_name, template_dirs=None):
        """ Add the resource dir to the available dirs. """
        res = thread_locals.resource
        if res:
            access_instance = self._access.objects.filter(resource=res).first()
            path = access_instance.get_path('templates')
            template_dirs = (path,) + (template_dirs or ())

        return super(TemplationLoader, self).get_template_sources(template_name,
                                                                  template_dirs)
