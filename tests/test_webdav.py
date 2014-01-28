#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import unittest
import base64
from django.contrib.auth import get_user_model
from django.conf import settings
from webtest import TestApp, AppError


from templation.models import ResourceAccess
from tests.models import MyResource


class TestWebDav(unittest.TestCase):

    def setUp(self):
        # Load assets
        if os.access(settings.TEMPLATION_DAV_ROOT, os.W_OK):
            shutil.rmtree(settings.TEMPLATION_DAV_ROOT)
        shutil.copytree(os.path.join(os.path.dirname(__file__), 'fixtures/dav'), settings.TEMPLATION_DAV_ROOT)
        from templation.middleware import wsgidav_app
        self.application = wsgidav_app

        # Create user
        User = get_user_model()
        try:
            self.user = User.objects.get(username='john', email='john@johnny.com')
        except User.DoesNotExist:
            self.user = User.objects.create_user(username='john', email='john@johnny.com', password='top_secret')
        self.user_auth = 'Basic ' + base64.encodestring('john:top_secret').replace('\n', '')

        # Create WebDav Access
        self.resource = MyResource.objects.get_or_create(name='Foo', id=1234)[0]
        ResourceAccess.objects.create(user=self.user, resource=self.resource)

    def test_list_ok(self):
        app = TestApp(self.application)
        response = app.get('/templation/1/1234/', [], [('Authorization', self.user_auth)])
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_list(self):
        app = TestApp(self.application)
        try:
            app.get('/templation/1/1337/', [], [('Authorization', self.user_auth)])
        except AppError as e:
            self.assertTrue(e.message.startswith("Bad response: 401 Not Authorized"))
