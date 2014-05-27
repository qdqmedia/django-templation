#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import BaseTest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest
from django.template import TemplateSyntaxError
from templation.templatetags.templation_tags import static, get_model_info, is_trusted_request
from templation.locals import thread_locals


class TestTemplationTemplateTags(BaseTest):

    def test_static_normal_user(self):
        self.assertEquals(static('js/main.js'), '/static/js/main.js')

    def test_static_designer(self):
        thread_locals.user = self.user
        thread_locals.resource = self.resource
        self.assertEquals(static('js/main.js'), '{0}1234/js/main.js'.format(settings.TEMPLATION_DAV_STATIC_URL))

    def test_static_validated_resource(self):
        thread_locals.user = AnonymousUser()
        thread_locals.resource = self.resource
        self.assertEquals(static('js/main.js'), '{0}1234/js/main.js'.format(settings.TEMPLATION_DAV_STATIC_URL))

    def test_get_model_info(self):
        for thing in (User.objects.all(), User()):
            self.assertEquals(
                get_model_info(thing), {'model_name': 'user', 'app_label': 'auth'}
            )

        self.assertRaises(
            TemplateSyntaxError,
            lambda: get_model_info(object()),
        )

    def test_is_trusted_request(self):
        user = User(username='test_user', is_active=True, is_staff=True)
        request = HttpRequest()
        request.user = user
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        context = {'request': request}
        self.assertTrue(is_trusted_request(context))
        user.is_active = False
        self.assertFalse(is_trusted_request(context))
        user.is_active = True
        user.is_staff = False
        self.assertFalse(is_trusted_request(context))
        request.META['REMOTE_ADDR'] = '1.2.3.4'
        self.assertFalse(is_trusted_request(context))
