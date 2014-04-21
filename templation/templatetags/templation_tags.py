from __future__ import absolute_import
from django import template
from django.conf import settings
from django.db.models import Model
from django.db.models.query import QuerySet
from django.template import TemplateSyntaxError
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


@register.assignment_tag
def get_model_info(thing):
    if isinstance(thing, Model):
        meta = thing._meta
    elif isinstance(thing, QuerySet):
        meta = thing.model._meta
    else:
        raise TemplateSyntaxError('Wrong paramer type for %s' % str(thing))

    app_label = meta.app_label
    model_name = getattr(meta, 'model_name', None) or \
        getattr(meta, 'module_name').lower()  # meta.model_name is for Django < 1.6 compatibility

    return {
        'app_label': app_label,
        'model_name': model_name,
    }


@register.assignment_tag(takes_context=True)
def is_trusted_request(context):
    request = context['request']
    return request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS or (request.user.is_active and request.user.is_staff)
