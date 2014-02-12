"""
Mixin to add in your CCBV to store the object.pk as resource to be fetched in the template.
"""
from __future__ import absolute_import
from .locals import thread_locals


class ResourceStoreMixin(object):
    """
    Addicted to Class Based Views? we too! here you had a mixin
    to add to any DetailView to handle custom templates.

    If you can't rely con `self.object` or kwargs['pk'] to get the instance,
    override `get_templation_object()`to return a instance of the resource in
    `templation.settings.get_resource_model()`.
    """
    def get_templation_object(self, *args, **kwargs):
        return getattr(self, 'object', getattr(kwargs, 'pk', None))

    def dispatch(self, request, *args, **kwargs):
        context = super(ResourceStoreMixin, self).dispatch(request, *args, **kwargs)
        thread_locals.resource = self.get_templation_object(**kwargs)
        return context
