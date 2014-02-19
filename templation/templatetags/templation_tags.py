from __future__ import absolute_import
from django import template
from django.conf import settings
from django.templatetags.static import StaticNode
from django.contrib.staticfiles.storage import staticfiles_storage
from ..settings import DAV_STATIC_URL
from ..locals import thread_locals
from ..utils import will_override

register = template.Library()


def templation_url(url):
    """
    Prefixes url with DAV_STATIC_URL
    """

    override, _ = will_override()

    if override:
        url = '/'.join((DAV_STATIC_URL.rstrip('/'),
                        str(thread_locals.resource.id),
                        url.split(settings.STATIC_URL, 1)[1].lstrip('/')))
    return url


class StaticFilesNode(StaticNode):

    def url(self, context):
        path = self.path.resolve(context)
        static_url = staticfiles_storage.url(path)
        return templation_url(static_url)


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
    return templation_url(staticfiles_storage.url(path))
