"""
Wrapper for loading templates from the filesystem.
"""

from __future__ import absolute_import
from django.template.base import Template
from django.template.loaders.app_directories import Loader
from .settings import get_resource_access_model, SANDBOX_TEMPLATES
from .utils import will_override, use_safe_templates


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

    def load_template(self, template_name, template_dirs=None):
        source, origin = self.load_template_source(template_name, template_dirs)
        override, _ = will_override()
        if SANDBOX_TEMPLATES and override:
            template = use_safe_templates(Template)(source)
        else:
            template = Template(source)
        return template, origin
