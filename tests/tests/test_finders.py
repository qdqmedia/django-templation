#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.auth.models import AnonymousUser
from . import BaseTest
from templation.settings import DAV_ROOT
from templation.locals import thread_locals


class TestStaticFinder(BaseTest):

    def setUp(self):
        super(TestStaticFinder, self).setUp()
        self.finder = finders.get_finder('templation.finders.TemplationStaticFinder')

    def test_list(self):
        static_files = sorted((e[0] for e in self.finder.list([])))
        real_statics = []
        for root, dirs, files in os.walk(self.resource_access.get_path('static'), False):
            if files:
                real_statics.extend([os.path.join(root, f).split(DAV_ROOT, 1)[1] for f in files])

        self.assertEqual(static_files, sorted(real_statics))

    def test_find_as_staff(self):
        thread_locals.user = self.user
        thread_locals.resource = self.resource
        static_file = self.finder.find('js/main.js')
        self.assertEqual(static_file, os.path.join(DAV_ROOT, '1234/static/js/main.js'))

    def test_find_as_non_logged_user(self):
        try:
            # Simulate collect static
            old_static = settings.STATIC_ROOT.rstrip('/') + '_old'
            shutil.move(settings.STATIC_ROOT, old_static)
            shutil.copytree(DAV_ROOT, settings.STATIC_ROOT)

            thread_locals.user = AnonymousUser()
            thread_locals.resource = self.resource
            static_file = self.finder.find('js/main.js')
            self.assertEqual(static_file, os.path.join(settings.STATIC_ROOT, '1234/static/js/main.js'))
        finally:
            # Destroy collectstatic
            if os.path.exists(old_static) and os.path.exists(settings.STATIC_ROOT):
                shutil.rmtree(settings.STATIC_ROOT)
                shutil.move(old_static, settings.STATIC_ROOT)
