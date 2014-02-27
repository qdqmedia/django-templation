#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from webtest import AppError
from templation.settings import DAV_ROOT
from . import BaseTest


class TestWebDav(BaseTest):

    def test_list_ok(self):
        response = self.app.get('/templation/1234/', [], [('Authorization', self.user_auth)])
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_list(self):
        try:
            self.app.get('/templation/1337/', [], [('Authorization', self.user_auth)])
        except AppError as e:
            self.assertTrue(e.message.startswith("Bad response: 401 Not Authorized"))

    def test_unregistered(self):
        try:
            self.app.get('/templation/1234/')
        except AppError as e:
            self.assertTrue(e.message.startswith("Bad response: 401 Not Authorized"))

    def test_create_file_ok(self):
        response = self.app.request('/templation/1234/hello_world.txt',
                                    method='PUT',
                                    headers=[('Authorization', self.user_auth)],
                                    body='Hello World!')
        self.assertEqual(response.status_code, 201)
        uploaded_to = os.path.join(DAV_ROOT, '1234/hello_world.txt')
        self.assertTrue(os.path.exists(uploaded_to))
        with open(uploaded_to) as f:
            file_content = f.read()
            self.assertEqual(file_content, 'Hello World!')

    def test_create_file_more_length(self):
        response = self.app.request('/templation/1234/hello_world.txt',
                                    method='PUT',
                                    headers=[
                                        ('Authorization', self.user_auth),
                                        ('Content-Length', '1024'),
                                    ],
                                    body='Hello World!')
        self.assertEqual(response.status_code, 201)
        uploaded_to = os.path.join(DAV_ROOT, '1234/hello_world.txt')
        self.assertTrue(os.path.exists(uploaded_to))
        with open(uploaded_to) as f:
            file_content = f.read()
            self.assertEqual(file_content, 'Hello World!')

    def test_create_file_less_length(self):
        response = self.app.request('/templation/1234/hello_world.txt',
                                    method='PUT',
                                    headers=[
                                        ('Authorization', self.user_auth),
                                        ('Content-Length', '1'),
                                    ],
                                    body='Hello World!')
        self.assertEqual(response.status_code, 201)
        uploaded_to = os.path.join(DAV_ROOT, '1234/hello_world.txt')
        self.assertTrue(os.path.exists(uploaded_to))
        with open(uploaded_to) as f:
            file_content = f.read()
            self.assertEqual(file_content, 'H')

    def test_boilerplate_copy(self):
        response = self.app.get('/templation/1234/response.txt', [], [('Authorization', self.user_auth)])
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response._app_iter, ['ok\n'])
