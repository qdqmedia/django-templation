#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import SetUpAccess


class TestResourceAccess(SetUpAccess):
    def test_webdav_path(self):
        self.assertEqual(self.resource_access.get_absolute_url(), '/templation/1234/')
