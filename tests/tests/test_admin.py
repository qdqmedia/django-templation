#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from . import BaseTest


class TestAdmin(BaseTest):

    def test_resourceaccess_list(self):
        response = self.client.get(reverse('admin:templation_resourceaccess_changelist'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_resourceaccess_detail(self):
        response = self.client.get(reverse('admin:templation_resourceaccess_change', args=(self.resource_access.id,)), follow=True)
        self.assertEqual(response.status_code, 200)
