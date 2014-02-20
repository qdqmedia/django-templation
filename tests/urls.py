from django.conf.urls import patterns, url, include
from django.contrib import admin
from templation.urls import templation_static
from .views import *

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/(?P<pk>\d+)/$', index, name='index'),
    url(r'^cbv_index/(?P<pk>\d+)/$', IndexView.as_view(), name='cbv_index'),
    url(r'^extended/(?P<pk>\d+)/$', ExtendedView.as_view(), name='extended'),
    url(r'^fail/(?P<pk>\d+)/$', FailView.as_view(), name='fail'),
    url(r'^public_connection/$', PublicView.as_view(), name='public'),
) + templation_static()
