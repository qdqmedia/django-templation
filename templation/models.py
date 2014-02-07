# -*- coding: utf-8 -*-
import os
import shutil
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .settings import DAV_ROOT, PROVIDER_NAME, BOILERPLATE_INITIALIZER, \
    get_resource_model, BOILERPLATE_FOLDER, import_from_path


class ResourceAccessManager(models.Manager):

    def filter_validated(self, *args, **kwargs):
        return self.filter(is_validated=True, *args, **kwargs)


class AbstractResourceAccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    resource = models.ForeignKey(get_resource_model())
    is_validated = models.BooleanField(default=False)

    objects = ResourceAccessManager()

    class Meta:
        abstract = True
        verbose_name = _('ResourceAccess')
        verbose_name_plural = _('ResourceAccesses')
        unique_together = ('user', 'resource')

    def get_absolute_url(self):
        """Returns the WebDav path for this resource."""

        return os.path.join('/' + PROVIDER_NAME, str(self.resource.id)) + '/'

    def get_path(self, append=None):
        if append and not append.endswith('/'):
            append += '/'
        return os.path.join(DAV_ROOT, str(self.resource.id), append)


class ResourceAccess(AbstractResourceAccess):
    """Resource Access Model."""


def copy_boilerplate_folder(user_dir):
    """
    Default behavior to initialize the webdav folder. copy the resources from
    `settings.TEMPLATION_BOILERPLATE_FOLDER` to the newly created folder.
    Overridable function with `settings.TEMPLATION_BOILERPLATE_INITIALIZER`.
    """

    if os.path.isdir(BOILERPLATE_FOLDER):
        shutil.rmtree(user_dir)  # copytree needs to create the dir...
        shutil.copytree(BOILERPLATE_FOLDER, user_dir)
    elif BOILERPLATE_FOLDER:   # pragma no cover
        raise ValueError('{} is not a valid directory'.format(BOILERPLATE_FOLDER))


def create_resource_access(sender, instance, created, **kwargs):
    if created:
        try:
            user_dir = os.path.join(DAV_ROOT, str(instance.resource.id))
            # create in case neither folder or initializer are defined.
            os.makedirs(user_dir)
            import_from_path(BOILERPLATE_INITIALIZER)(user_dir)
        except OSError as e:  # pragma no cover
            if e.errno != 17:
                raise

post_save.connect(create_resource_access, sender=ResourceAccess)
