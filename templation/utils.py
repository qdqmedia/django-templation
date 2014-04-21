# -*- coding: utf-8 -*-
from django.utils.functional import wraps
from django import template
from .locals import thread_locals
from .settings import get_resource_access_model, WHITELIST_TAGS, WHITELIST_FILTERS, EXTRA_LIBRARIES
from importlib import import_module

def will_override():
    """
    Test the necessary conditions for a template to be overwritten

    :returns: (bool, resource_access)
    """
    _access = get_resource_access_model()
    try:
        resource_access = _access.objects.filter(resource=thread_locals.resource)[:1][0]
    except IndexError:
        resource_access = None
    ret_value = (resource_access and
                (resource_access.is_validated or
                (resource_access.validate_access_token(thread_locals.token)) or
                (thread_locals.user.is_staff and _access.objects.filter(user=thread_locals.user,
                                                                        resource=thread_locals.resource))))
    return (ret_value, resource_access)


# Django snippet to whitelist template tags
# https://djangosnippets.org/snippets/2750/

def use_safe_templates(tags=None, filters=None, extra=None):
    """
    Cleans the builtin template libraries before running the function (restoring
    the builtins afterwards).

    Removes any builtin tags and filters that are not enumerated in `tags` and
    `filters`, and adds the extra library modules in `extra` to the builtins.

    Does not catch any template exceptions (notably, TemplateSyntaxError and
    TemplateDoesNotExist may be raised).
    """
    def decorate(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            # Clean out default libraries
            # Note: template.builtins is merely a convenience import, we have to work
            # with template.base.builtins for this to work right.
            template.base.builtins, default_libs = [], template.base.builtins
            try:
                # Construct new builtin with only whitelisted tags/filters
                whitelist = template.Library()
                for lib in default_libs:
                    for tag in lib.tags:
                        if tag in tags:
                            whitelist.tags[tag] = lib.tags[tag]
                    for filter in lib.filters:
                        if filter in filters:
                            whitelist.filters[filter] = lib.filters[filter]

                # Install whitelist library and extras as builtins
                template.base.builtins.append(whitelist)
                [template.add_to_builtins(e) for e in extra]

                return func(*args, **kwargs)
            finally:
                # Restore the builtins to their former defaults
                template.base.builtins = default_libs
        return wrapped

    # @use_safe_templates
    func = tags
    tags = WHITELIST_TAGS
    filters = WHITELIST_FILTERS
    extra = EXTRA_LIBRARIES
    return decorate(func)


def get_class(module_name, cls_name):
    """Grab a class reference given its module and name"""
    try:
        module = import_module(module_name)
        return getattr(module, cls_name)
    except ImportError:
        raise ImportError('Invalid class path: {0}'.format(module_name))
    except AttributeError:
        raise ImportError('Invalid class name: {0}'.format(cls_name))
