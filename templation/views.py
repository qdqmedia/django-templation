"""
Mixin to add in your CCBV to store the object.pk as resource to be fetched in the template.
"""
from .locals import thread_locals
from django.views.generic.detail import SingleObjectMixin


class ResourceStoreMixin(object):
    def dispatch(self, request, *args, **kwargs):
        assert isinstance(self, SingleObjectMixin), 'ResourceStoreMixin is not descendant of SingleObjectMixin.'
        thread_locals.resource = self.get_object()
        super(ResourceStoreMixin, self).dispatch(request, *args, **kwargs)
