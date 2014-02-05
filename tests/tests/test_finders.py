#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from django.contrib.staticfiles import finders
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

    def test_find(self):
        thread_locals.user = self.user
        static_file = self.finder.find('1234/js/main.js')
        self.assertEqual(static_file, '/tmp/dav/1234/static/js/main.js')
