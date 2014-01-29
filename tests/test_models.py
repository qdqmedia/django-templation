#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from django.contrib.auth import get_user_model
from templation.models import ResourceAccess
from tests.models import MyResource


class TestResourceAccess(unittest.TestCase):

    def setUp(self):

        # Create user
        User = get_user_model()
        self.user = User.objects.create_user(username='john', email='john@johnny.com', password='top_secret')

        # Create WebDav Access
        self.resource = MyResource.objects.create(name='Foo', id=1234)
        self.resource_access = ResourceAccess.objects.create(user=self.user, resource=self.resource)

    def test_webdav_path(self):
        self.assertEqual(self.resource_access.get_absolute_url(), '/templation/1234/')

    def tearDown(self):
        self.resource_access.delete()
        self.resource.delete()
        self.user.delete()
