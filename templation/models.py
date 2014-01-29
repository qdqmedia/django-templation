# -*- coding: utf-8 -*-
import os.path
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from .settings import DAV_ROOT, PROVIDER_NAME, RESOURCE_MODEL


class AbstractResourceAccess(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    resource = models.ForeignKey(RESOURCE_MODEL)

    class Meta:
        abstract = True
        verbose_name = _('ResourceAccess')
        verbose_name_plural = _('ResourceAccesses')
        unique_together = ('user', 'resource')

    def get_absolute_url(self):
        """
        Returns the WebDav path for this resource
        """

        return os.path.join('/' + PROVIDER_NAME, str(self.resource.id)) + '/'


class ResourceAccess(AbstractResourceAccess):
    """
    Resource Access Model
    """


def create_resource_access(sender, instance, created, **kwargs):
    if created:
        # Initialize folders (TODO: copy template)
        try:
            os.makedirs(os.path.join(DAV_ROOT, str(instance.resource.id)))
        except OSError as e:
            if e.errno != 17:
                raise

post_save.connect(create_resource_access, sender=ResourceAccess)
