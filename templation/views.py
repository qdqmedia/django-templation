"""
Mixin to add in your CCBV to store the object.pk as resource to be fetched in the template.
"""
from .locals import thread_locals
from django.views.generic.detail import SingleObjectMixin


class ResourceStoreMixin(object):
    """
    Addicted to Class Based Views? we too! here you had a mixin
    to add to any DetailView to handle custom templates.

    If you can't rely con `self.object` override `get_templation_object()`
    to return a instance of the resource in
    `templation.settings.get_resource_model()`.
    """
    def get_templation_object(self):
        assert isinstance(self, SingleObjectMixin), 'ResourceStoreMixin is not descendant of SingleObjectMixin.'
        return self.object or self.get_object()

    def dispatch(self, request, *args, **kwargs):
        thread_locals.resource = self.get_templation_object()
        return super(ResourceStoreMixin, self).dispatch(request, *args, **kwargs)
