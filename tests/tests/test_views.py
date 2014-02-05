#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import BaseTest


class TestIndex(BaseTest):

    def test_template_loader(self):
        response = self.client.get('/index/{}/'.format(self.resource.id), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEquals(response.content, 'NOT OVERRIDEN\n')

    def test_cbv_template_loader(self):
        response = self.client.get('/cbv_index/{}/'.format(self.resource.id), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEquals(response.content, 'NOT OVERRIDEN\n')
