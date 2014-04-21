from . import BaseTest
from django.http import HttpRequest
from templation.context_processor import templation_info

class TestTemplationTemplateTags(BaseTest):

    def test_templation_info(self):
        """This just makes sure that templation_info passes through all it gets"""
        request = HttpRequest()
        request._templation_view = 'foo'
        request._templation_template = 'bar'

        self.assertEqual(
            templation_info(request), {'templation_view': 'foo', 'templation_template': 'bar'}
        )

