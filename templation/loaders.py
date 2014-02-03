"""
Wrapper for loading templates from the filesystem.
"""

from threading import local
from django.conf import settings
from django.template.base import TemplateDoesNotExist
from django.template import loader
from django.utils._os import safe_join

thread_vars = local()


class TemplationLoader(loader.app_directories.Loader):

    def get_template_sources(self, template_name, template_dirs=None):
        pass

    def load_template_sources(self, template_name, template_dirs=None):
        pass
