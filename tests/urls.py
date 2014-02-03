from django.conf.urls import patterns, url
from .views import index

urlpatterns = patterns(
    '',
    url(r'^index/(?P<pk>\d+)/$', index, name='index'),
)
