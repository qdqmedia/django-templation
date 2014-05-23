from __future__ import absolute_import
import logging
from django.contrib.auth import authenticate
from django.conf import settings
from wsgidav.wsgidav_app import DEFAULT_CONFIG
from wsgidav.wsgidav_app import WsgiDAVApp
from .settings import DAV_ROOT, PROVIDER_NAME, get_resource_access_model
from .locals import thread_locals
from .utils import get_class

logger = logging.getLogger(__name__)


class TemplationDomainController(object):
    def requireAuthentication(self, realmname, environ):
        return True

    def getDomainRealm(self, inputRelativeURL, environ):
        return environ.get('PATH_INFO').split('/')[1]

    def authDomainUser(self, realmname, username, password, environ):
        user = authenticate(username=username, password=password)
        try:
            return get_resource_access_model().objects.get(user=user, resource_pointer__resource__id=realmname)
        except get_resource_access_model().DoesNotExist:
            return False

config = DEFAULT_CONFIG.copy()
config.update({
    'provider_mapping': {PROVIDER_NAME: DAV_ROOT},
    'user_mapping': {DAV_ROOT: {None: None}},
    'domaincontroller': TemplationDomainController(),
    'acceptdigest': False,
    'defaultdigest': False,
})

wsgidav_app = WsgiDAVApp(config)


class WsgiDAVMiddleware(object):
    def __init__(self, django_app):
        self.django_app = django_app

    def __call__(self, environ, start_response):
        if environ.get('PATH_INFO').startswith('/' + PROVIDER_NAME.strip('/') + '/'):
            return wsgidav_app(environ, start_response)
        return self.django_app(environ, start_response)


class TemplationMiddleware(object):

    def process_request(self, request):
        thread_locals.user = getattr(request, 'user', None)
        thread_locals.token = request.GET.get('tt', '') or request.COOKIES.get('tt', '')

    def process_response(self, request, response):
        if thread_locals.token:
            response.set_cookie(key='tt', value=thread_locals.token)
        thread_locals.clear()
        return response

    def process_exception(self, request, exception):
        thread_locals.clear()  # leave a clean state

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS or (request.user.is_active and request.user.is_staff):
            request._templation_view = "{0}.{1}".format(view_func.__module__, view_func.__name__)
            try:
                view_cls = get_class(view_func.__module__, view_func.__name__)
            except ImportError:
                pass
            else:
                if hasattr(view_cls, 'template_name'):
                    request._templation_template = view_cls.template_name
