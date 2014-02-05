#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import base64
import unittest
from django.contrib.auth import get_user_model
from django.test.client import Client
from webtest import TestApp
from templation import settings


class SetUpFolders(unittest.TestCase):
    def setUp(self):
        if os.access(settings.DAV_ROOT, os.W_OK):
            shutil.rmtree(settings.DAV_ROOT)
        os.makedirs(settings.DAV_ROOT)
        from templation.middleware import wsgidav_app
        self.application = wsgidav_app
        self.app = TestApp(self.application)

        super(SetUpFolders, self).setUp()


class SetUpAccess(unittest.TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username='john',
            email='john@doe.com',
        )
        self.user.set_password('secret')
        self.user.is_staff = True
        self.user.save()

        self.user_auth = 'Basic ' + \
            base64.encodestring('john:secret').replace('\n', '')

        self.resource = settings.get_resource_model().objects.create(name='Foo', id=1234)
        self.resource_access = settings.get_resource_access_model().objects.create(user=self.user, resource=self.resource, is_validated=True)

        self.client = Client()
        self.client.login(username=self.user.username, password='secret')
        super(SetUpAccess, self).setUp()

    def tearDown(self):
        self.user.delete()
        self.resource.delete()
        self.resource_access.delete()

        super(SetUpAccess, self).tearDown()


class SetUpTemplateDump(unittest.TestCase):
    def setUp(self):
        super(SetUpTemplateDump, self).setUp()


class BaseTest(SetUpFolders, SetUpAccess, SetUpTemplateDump):
    """ FullStack of setUps and teardowns """
