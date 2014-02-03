import os
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseFinder
from django.utils._os import safe_join
from django.conf import settings
from .settings import DAV_ROOT


class TemplationStaticFinder(BaseFinder):
    """
    A static finder that serves a different path depending on
    the user.
    """

    storage = FileSystemStorage(DAV_ROOT, settings.STATIC_URL)

    def __init__(self, apps=None, *args, **kwargs):
        # List of locations with static files
        self.locations = []
        for resource_dir in os.listdir(DAV_ROOT):
            self.locations.append(os.path.join(DAV_ROOT, resource_dir))

        super(TemplationStaticFinder, self).__init__(*args, **kwargs)

    def find(self, path, all=False):
        """
        Looks for files in the webdav dirs.
        Path must start with the prefix "/templation/<user_id>/

        In example: /templation/1234/css/bootstrap.css
        """
        matches = []

        # Remove unused prefix
        split_path = path.split('/')
        user_id = split_path[2]
        path = split_path[3:]
        matched_path = self.find_location(DAV_ROOT, path, user_id)
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
        for root in self.locations:
            for path in utils.get_files(self.storage, ignore_patterns):
                yield path, self.storage
