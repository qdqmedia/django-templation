# -*- coding: utf-8 -*-
from .locals import thread_locals
from .settings import get_resource_access_model


def will_override():
    """
    Test the necessary conditions for a template to be overwritten

    :returns: (bool, resource_access)
    """
    _access = get_resource_access_model()
    resource_access = _access.objects.filter(resource=thread_locals.resource).first()
    ret_value = (resource_access and
                (resource_access.is_validated or
                (resource_access.validate_access_token(thread_locals.token)) or
                (thread_locals.user.is_staff and _access.objects.filter(user=thread_locals.user,
                                                                        resource=thread_locals.resource))))
    return (ret_value, resource_access)
