"""
Mixin to add in your CCBV to store the object.pk as resource to be fetched in the template.
"""
from .locals import thread_locals
from .settings import get_resource_access_model


class ResourceStoreMixin(object):
    """
    Addicted to Class Based Views? we too! here you had a mixin
    to add to any DetailView to handle custom templates.

    If you can't rely con `self.object` override `get_templation_object()`
    to return a instance of the resource in
    `templation.settings.get_resource_model()`.
    """
    def get_templation_object(self, *args, **kwargs):
        return getattr(self, 'object', getattr(kwargs, 'pk', None))

    def dispatch(self, request, *args, **kwargs):
        context = super(ResourceStoreMixin, self).dispatch(request, *args, **kwargs)
        thread_locals.resource = self.get_templation_object(**kwargs)
        return context
