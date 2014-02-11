from django import template
from django.conf import settings
from django.core.cache import cache
from django.templatetags.static import StaticNode
from django.contrib.staticfiles.storage import staticfiles_storage
from ..settings import get_resource_access_model, VALIDATED_IDS_CACHE_TIME, DAV_STATIC_URL
from ..locals import thread_locals

register = template.Library()


def validated_ids(self):
    cache_key = self.__class__.__name__ + ':validated_ids'
    result = cache.get(cache_key)
    if not result:
        result = set(map(str, get_resource_access_model().objects.filter_validated().values_list('resource__id', flat=True)))
        cache.set(cache_key, result, VALIDATED_IDS_CACHE_TIME)
    return result


class StaticFilesNode(StaticNode):

    def url(self, context):
        path = self.path.resolve(context)
        static_url = staticfiles_storage.url(path)
        resource_access = get_resource_access_model().objects.filter(resource=thread_locals.resource).first()
        if resource_access and resource_access.is_validated or get_resource_access_model().objects.filter(user=thread_locals.user, resource=thread_locals.resource):
            static_url = '/'.join((DAV_STATIC_URL.rstrip('/'),
                                   str(thread_locals.resource.id),
                                   static_url.split(settings.STATIC_URL, 1)[1].lstrip('/')))
        return static_url


@register.tag('static')
def do_static(parser, token):
    """
    A template tag that returns the URL to a file
    using staticfiles' storage backend

    Usage::

        {% static path [as varname] %}

    Examples::

        {% static "myapp/css/base.css" %}
        {% static variable_with_path %}
        {% static "myapp/css/base.css" as admin_base_css %}
        {% static variable_with_path as varname %}

    """
    return StaticFilesNode.handle_token(parser, token)


def static(path):
    return staticfiles_storage.url(path)
