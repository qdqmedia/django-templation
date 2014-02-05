from django.conf.urls import patterns, url
from .views import index, IndexView

urlpatterns = patterns(
    '',
    url(r'^index/(?P<pk>\d+)/$', index, name='index'),
    url(r'^cbv_index/(?P<pk>\d+)/$', IndexView.as_view(), name='index'),
)
