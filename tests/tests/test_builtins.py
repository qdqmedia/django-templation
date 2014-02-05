import unittest
from django.template.base import builtins


class BuiltinsTest(unittest.TestCase):

    def test_deleted_tag(self):
        self.assertFalse('load' in builtins[1].tags)

    def test_deleted_filters(self):
        self.assertFalse('exclude' in builtins[2].filters)
