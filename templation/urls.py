from django.conf.urls import patterns, url
from .settings import DAV_ROOT, DAV_STATIC_URL
from .views import static_view


def templation_static(**kwargs):
    """
    Helper function to return a URL pattern for serving files in debug mode.
    Mostly cloned from django.conf.urls.static function.

    from templation.urls import templation_static

    urlpatterns = patterns('',
        # ... the rest of your URLconf goes here ...
    ) + templation_static(**kwargs)

    """
    kwargs.update({
        'document_root': DAV_ROOT
    })

    return patterns(
        '',
        url(r'{0}/(?P<resource_id>\d+)/(?P<path>.*)$'.format(
            DAV_STATIC_URL.strip('/')), static_view, kwargs=kwargs),
    )
