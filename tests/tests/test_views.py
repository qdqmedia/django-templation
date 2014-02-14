#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template.base import TemplateSyntaxError
from django.conf import settings
from templation.settings import get_resource_model
from . import BaseTest


class TestIndex(BaseTest):

    def _assert_overriden(self, response):
        self.assertIn('<script src="{}1234/js/main.js"></script>'.format(settings.TEMPLATION_DAV_STATIC_URL), response.content)
        self.assertEqual(response.status_code, 200)
        self.assertNotEquals(response.content, 'NOT OVERRIDEN\n')

    def _assert_not_overriden(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.content, 'NOT OVERRIDEN\n')

    def test_template_loader_user_logged_validated_resource(self):
        response = self.client.get('/index/{}/'.format(self.resource.id), follow=True)
        self._assert_overriden(response)

    def test_template_loader_user_logged_not_validated_resource(self):
        response = self.client.get('/index/{}/'.format(self.resource.id), follow=True)
        self.resource_access.is_validated = False
        self.resource_access.save()
        self._assert_overriden(response)

    def test_template_loader_user_logged_not_resource_access(self):
        resource = get_resource_model().objects.create(name='Bar', id=6789)
        response = self.client.get('/index/{}/'.format(resource.id), follow=True)
        self._assert_not_overriden(response)

    def test_template_loader_user_not_logged_validated_resource(self):
        self.client.logout()
        response = self.client.get('/index/{}/'.format(self.resource.id), follow=True)
        self._assert_overriden(response)

    def test_template_loader_user_not_logged_not_validated_resource(self):
        self.client.logout()
        self.resource_access.is_validated = False
        self.resource_access.save()
        response = self.client.get('/index/{}/'.format(self.resource.id), follow=True)
        self._assert_not_overriden(response)

    def test_template_loader_user_not_logged_not_resource_access(self):
        self.client.logout()
        resource = get_resource_model().objects.create(name='Bar', id=6780)
        response = self.client.get('/index/{}/'.format(resource.id), follow=True)
        self._assert_not_overriden(response)

    def test_cbv_template_loader(self):
        response = self.client.get('/cbv_index/{}/'.format(self.resource.id),
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<script src="{}1234/js/main.js"></script>'.format(settings.TEMPLATION_DAV_STATIC_URL), response.content)
        self.assertNotEquals(response.content, 'NOT OVERRIDEN\n')

    def _expect_fail(self):
        self.client.get('/fail/{}/'.format(self.resource.id), follow=True)

    def test_cbv_template_fail_loader(self):
        self.assertRaises(TemplateSyntaxError, self._expect_fail)

    def test_public_connection(self):
        response = self.client.get('/public_connection/'.format(self.resource.id),
                                   follow=True)
        self.assertEqual(response.status_code, 200)

    def test_extension_and_inclusion(self):
        response = self.client.get('/extended/{}/'.format(self.resource.id),
                                   follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('included.html'.format(settings.TEMPLATION_DAV_STATIC_URL), response.content)
        self.assertNotEquals(response.content, 'NOT OVERRIDEN\n')
