#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import BaseTest


class TestIndex(BaseTest):

    def test_index_without_templation(self):
        response = self.client.get('/index/{}/'.format(self.resource.id), follow=True)
        import ipdb; ipdb.set_trace()
        self.assertEqual(response.status_code, 200)
