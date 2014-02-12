#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import BaseTest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from templation.templatetags.static import static
from templation.locals import thread_locals


class TestTemplationTemplateTags(BaseTest):

    def test_static_normal_user(self):
        self.assertEquals(static('js/main.js'), '/static/js/main.js')

    def test_static_designer(self):
        thread_locals.user = self.user
        thread_locals.resource = self.resource
        self.assertEquals(static('js/main.js'), '{}1234/js/main.js'.format(settings.TEMPLATION_DAV_STATIC_URL))

    def test_static_validated_resource(self):
        thread_locals.user = AnonymousUser()
        thread_locals.resource = self.resource
        self.assertEquals(static('js/main.js'), '{}1234/js/main.js'.format(settings.TEMPLATION_DAV_STATIC_URL))
