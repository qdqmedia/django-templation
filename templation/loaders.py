"""
Wrapper for loading templates from the filesystem.
"""

from __future__ import absolute_import
from django.template.loaders.app_directories import Loader
from .locals import thread_locals
from .settings import get_resource_access_model


class TemplationLoader(Loader):
    def __init__(self):
        self._access = get_resource_access_model()

    def get_template_sources(self, template_name, template_dirs=None):
        """ Add the resource dir to the available dirs. """
        resource_access = get_resource_access_model().objects.filter(resource=thread_locals.resource).first()
        if (resource_access and resource_access.is_validated or
           (thread_locals.user.is_staff and get_resource_access_model().objects.filter(user=thread_locals.user, resource=thread_locals.resource))):
                path = resource_access.get_path('templates')
                template_dirs = (path,) + (template_dirs or ())

        return super(TemplationLoader, self).get_template_sources(template_name,
                                                                  template_dirs)
