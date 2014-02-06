# -*- coding: utf-8 -*-
"""
Common entry point to store variables inside threads.
"""
from threading import local
from django.shortcuts import get_object_or_404
from .settings import get_resource_model
from templation.settings import get_resource_access_model


class LocalsManager(object):
    """
    Oh Nasty Hacks™... Since static finders and template loaders can't load
    the request without option to adapt, we need to keep the resource
    somewhere accesible.

    Usage:

    >>> from templation.locals import thread_locals

    >>> thread_locals.resource = primary_key  # this should fetch the instance and keep_it
    >>> thread_locals.resource = resource_instance  # This prevents double fetch.
    """

    def __init__(self):
        self._model = get_resource_model()
        self._access_model = get_resource_access_model()
        self.__locals__ = local()
        self.clear()

    def clear(self):
        self.__locals__.user = None
        self.__locals__.resource = None
        self.__locals__.resource_access = None

    @property
    def user(self):
        return self.__locals__.user

    @user.setter
    def user(self, value):
        self.__locals__.user = value

    @property
    def resource(self):
        return self.__locals__.resource

    @resource.setter
    def resource(self, value):
        if isinstance(value, self._model):
            self.__locals__.resource = value
        else:
            self.__locals__.resource = get_object_or_404(self._model, pk=value)

    @property
    def resource_access(self):
        if not self.__locals__.resource_access:
            try:
                self.__locals__.resource_access = self._access_model.objects.get(user=self.user, resource=self.resource)
            except self._access_model.DoesNotExist:
                pass
            
        return self.__locals__.resource_access

    @resource_access.setter
    def resource_access(self, value):
        self.__locals__.resource_access = value


thread_locals = LocalsManager()
