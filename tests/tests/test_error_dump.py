#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test.utils import override_settings
from . import BaseTest


class TestErrorDump(BaseTest):

    def _assert_display_error(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertIn('', response.content)

    def _assert_hide_error(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertIn('', response.content)

    @override_settings(DEBUG=False)
    def test_dump_ok(self):
        response = self.client.get('/dump_ok/{}/'.format(self.resource.id), follow=True)
        self._assert_display_error(response)

    @override_settings(DEBUG=True)
    def test_dump_ko(self):
        response = self.client.get('/dump_ko/{}/'.format(self.resource.id), follow=True)
        self._assert_hide_error(response)

    @override_settings(TEMPLATION_DEBUG=True)
    def test_dump(self):
        response = self.client.get('/index/{}/'.format(self.resource.id), follow=True)
        self._assert_display_error(response)

