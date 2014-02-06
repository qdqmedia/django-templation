import sys
import logging
from django.contrib.auth import authenticate
from wsgidav.wsgidav_app import DEFAULT_CONFIG
from wsgidav.wsgidav_app import WsgiDAVApp
from django.views import debug
from .settings import get_resource_access_model, import_from_path, \
    DEBUG, DUMP_REPORT_STRATEGY, DUMP_EXCEPTIONS, DAV_ROOT, PROVIDER_NAME
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


def dump_report_strategy(request):
    """
    Default Strategy to show errors only if django authenticated user is on
    templation Resource Model. You can customize this behavior with
    `settings.TEMPLATION_DUMP_REPORT_STRATEGY` and point to a custom function
    like:

    def customReportStrategy(request):
        return True
    """
    return bool(get_resource_access_model().objects.filter(user=request.user))


class TemplationMiddleware(object):
    def __init__(self):
        self.strategy = import_from_path(DUMP_REPORT_STRATEGY)

    def process_request(self, request):
        thread_locals.user = request.user

    def process_response(self, request, response):
        thread_locals.clear()
        return response

    def process_exception(self, request, exception):
        thread_locals.clear()
        if DEBUG or exception in DUMP_EXCEPTIONS and self.strategy(request):
            exc_info = sys.exc_info()
            exc_info.update({
                # remove the following info.
            })
            return debug.technical_500_response(request, *exc_info)
