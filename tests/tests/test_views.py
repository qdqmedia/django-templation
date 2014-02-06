#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import BaseTest
from django.template.base import TemplateSyntaxError


class TestIndex(BaseTest):

    def test_template_loader(self):
        response = self.client.get('/index/{}/'.format(self.resource.id), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEquals(response.content, 'NOT OVERRIDEN\n')

    def test_cbv_template_loader(self):
        response = self.client.get('/cbv_index/{}/'.format(self.resource.id),
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEquals(response.content, 'NOT OVERRIDEN\n')

    def _expect_fail(self):
        self.client.get('/fail/{}/'.format(self.resource.id), follow=True)

    def test_cbv_template_loader(self):
        self.assertRaises(TemplateSyntaxError, self._expect_fail)

    def test_public_connection(self):
        response = self.client.get('/public_connection/'.format(self.resource.id),
                                   follow=True)
        self.assertEqual(response.status_code, 200)