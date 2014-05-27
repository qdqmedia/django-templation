#!/usr/bin/env python
# -*- coding: utf-8 -*-

from templation.settings import get_resource_access_model
from . import SetUpAccess


class TestResourceAccess(SetUpAccess):
    def test_webdav_path(self):
        self.assertEqual(self.resource_access.get_absolute_url(),
                         '/templation/1234/')

    def test_validated(self):
        self.assertTrue(get_resource_access_model().objects.filter_validated())
