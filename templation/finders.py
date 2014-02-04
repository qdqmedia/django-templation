import os
from threading import local
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseFinder
from django.utils._os import safe_join
from django.conf import settings
from .settings import DAV_ROOT, get_resource_access_model

_thread_vars = local()


class TemplationStaticFinder(BaseFinder):
    """
    A static finder that serves a different path depending on
    the user.
    """

    locations = []
    storage = FileSystemStorage(DAV_ROOT, settings.STATIC_URL)

    def __init__(self, apps=None, *args, **kwargs):
        # List of locations with static files
        for resource_dir in os.listdir(DAV_ROOT):
            self.locations.append(os.path.join(DAV_ROOT, resource_dir))

        super(TemplationStaticFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Looks for files in the webdav dirs.
        """
        matches = []

        # Remove unused prefix
        matched_path = self.find_location(DAV_ROOT, path)
        if matched_path:
            if not all:
                return matched_path
            matches.append(matched_path)
        return matches

    def find_location(self, root, path, prefix=None):
        """
        Finds a requested static file in a location, returning the found
        absolute path (or ``None`` if no match).
        """
        if prefix:
            prefix = '%s%s' % (prefix, os.sep)
            if not path.startswith(prefix):
                return None
            path = path[len(prefix):]
        path = safe_join(root, path)
        if os.path.exists(path):
            return path

    def list(self, ignore_patterns):
        """
        List all files in all locations.
        """
        validated_ids = set(get_resource_access_model().objects.filter_validated().values_list('resource__id', flat=True))
        for root in (e for e in self.locations if e.rsplit('/', 1)[-1] in validated_ids):
            for path in utils.get_files(self.storage, ignore_patterns):
                yield path, self.storage
