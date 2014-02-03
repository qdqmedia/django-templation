#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webtest import AppError
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

    def test_boilerplate_copy(self):
        response = self.app.get('/templation/1234/response.txt', [], [('Authorization', self.user_auth)])
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response._app_iter, ['ok\n'])
