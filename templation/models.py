# -*- coding: utf-8 -*-
import os.path
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .settings import DAV_ROOT, RESOURCE_MODEL


class ResourceAccess(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    resource = models.ForeignKey(RESOURCE_MODEL)

    class Meta:
        verbose_name = _('ResourceAccess')
        verbose_name_plural = _('ResourceAccesses')

    @property
    def dav_path(self):
        """
        Returns the WebDav path for this resource
        """

        return os.path.join(DAV_ROOT, self.user.id, self.resource.id)
