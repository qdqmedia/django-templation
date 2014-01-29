#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import unittest
import base64
from django.contrib.auth import get_user_model
from django.conf import settings
from webtest import TestApp, AppError
from templation.settings import get_resource_access_model, get_resource_model


class TestWebDav(unittest.TestCase):

    def setUp(self):
        # Load assets
        if os.access(settings.TEMPLATION_DAV_ROOT, os.W_OK):
            shutil.rmtree(settings.TEMPLATION_DAV_ROOT)
        os.makedirs(settings.TEMPLATION_DAV_ROOT)
        from templation.middleware import wsgidav_app
        self.application = wsgidav_app

        # Create user
        User = get_user_model()
        self.user = User.objects.create_user(username='john', email='john@johnny.com', password='top_secret')
        self.user_auth = 'Basic ' + base64.encodestring('john:top_secret').replace('\n', '')

        # Create WebDav Access
        self.resource = get_resource_model().objects.create(name='Foo', id=1234)
        self.resource_access = get_resource_access_model().objects.create(user=self.user, resource=self.resource)

    def test_list_ok(self):
        app = TestApp(self.application)
        response = app.get('/templation/1234/', [], [('Authorization', self.user_auth)])
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_list(self):
        app = TestApp(self.application)
        try:
            app.get('/templation/1337/', [], [('Authorization', self.user_auth)])
        except AppError as e:
            self.assertTrue(e.message.startswith("Bad response: 401 Not Authorized"))

    def tearDown(self):
        self.resource_access.delete()
        self.resource.delete()
        self.user.delete()
