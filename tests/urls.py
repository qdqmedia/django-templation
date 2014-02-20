from django.conf.urls import patterns, url
from templation.urls import templation_static
from .views import *

urlpatterns = patterns(
    '',
    url(r'^index/(?P<pk>\d+)/$', index, name='index'),
    url(r'^cbv_index/(?P<pk>\d+)/$', IndexView.as_view(), name='cbv_index'),
    url(r'^extended/(?P<pk>\d+)/$', ExtendedView.as_view(), name='extended'),
    url(r'^fail/(?P<pk>\d+)/$', FailView.as_view(), name='fail'),
    url(r'^public_connection/$', PublicView.as_view(), name='public'),
) + templation_static()
