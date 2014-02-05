from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from .views import index, IndexView

urlpatterns = patterns(
    '',
    url(r'^index/(?P<pk>\d+)/$', index, name='index'),
    url(r'^cbv_index/(?P<pk>\d+)/$', IndexView.as_view(), name='index'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
