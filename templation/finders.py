import os
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseFinder
from django.conf import settings
from django.utils._os import safe_join
from .settings import DAV_ROOT, get_resource_access_model, VALIDATED_IDS_CACHE_TIME
from .locals import thread_locals


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

    @property
    def validated_ids(self):
        cache_key = self.__class__.__name__ + ':validated_ids'
        result = cache.get(cache_key)
        if not result:
            result = set(map(str, get_resource_access_model().objects.filter_validated().values_list('resource__id', flat=True)))
            cache.set(cache_key, result, VALIDATED_IDS_CACHE_TIME)
        return result

    def find(self, path, all=False):
        """
        Looks for files in the webdav dirs.
        """
        if getattr(thread_locals.user, 'is_staff', False) and get_resource_access_model().objects.filter(user=thread_locals.user, resource=thread_locals.resource):
            matched_path = self.find_location(os.path.join(DAV_ROOT, str(thread_locals.resource.id)), path, 'static')
            if matched_path:
                return [matched_path] if all else matched_path

        elif str(getattr(thread_locals.resource, 'id', '')) in self.validated_ids:
            matched_path = self.find_location(os.path.join(settings.STATIC_ROOT, str(thread_locals.resource.id)), path, 'static')
            if matched_path:
                return [matched_path] if all else matched_path

        return []

    def find_location(self, root, path, prefix=None):
        """
        Finds a requested static file in a location, returning the found
        absolute path (or ``None`` if no match).
        """
        if prefix:
            path = safe_join(root, prefix, path)
        else:
            path = safe_join(root, path)
        if os.path.exists(path):
            return path

    def list(self, ignore_patterns):
        """
        List all files in all locations.
        """
        for root in (e for e in self.locations if e.rsplit('/', 1)[-1] in self.validated_ids):
            for path in utils.get_files(self.storage, ignore_patterns):
                if path.split('/', 1)[1].startswith('static/'):
                    yield path, self.storage
