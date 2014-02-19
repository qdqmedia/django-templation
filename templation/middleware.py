from __future__ import absolute_import
import logging
from django.contrib.auth import authenticate
from wsgidav.wsgidav_app import DEFAULT_CONFIG
from wsgidav.wsgidav_app import WsgiDAVApp
from .settings import import_from_path, \
    DAV_ROOT, PROVIDER_NAME
from .models import ResourceAccess
from .locals import thread_locals

logger = logging.getLogger(__name__)


class TemplationDomainController(object):
    def requireAuthentication(self, realmname, environ):
        return True

    def getDomainRealm(self, inputRelativeURL, environ):
        return environ.get('PATH_INFO').split('/')[1]

    def authDomainUser(self, realmname, username, password, environ):
        user = authenticate(username=username, password=password)
        try:
            return ResourceAccess.objects.get(user=user, resource__id=realmname)
        except ResourceAccess.DoesNotExist:
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
        if environ.get('PATH_INFO').startswith('/' + PROVIDER_NAME):
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
