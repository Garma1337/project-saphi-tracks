# coding: utf-8

from unittest import TestCase

from api.database.dto_generator.htmlcodeformatter import HtmlCodeFormatter


class HtmlCodeFormatterTest(TestCase):

    def setUp(self):
        self.html_code_formatter = HtmlCodeFormatter()

    def test_can_format_code(self):
        code = 'def hello_world():\n\tprint("Hello, world!")'
        formatted_code = self.html_code_formatter.format_code(code)

        self.assertEqual(formatted_code, 'def hello_world():<br>&nbsp;&nbsp;&nbsp;&nbsp;print("Hello, world!")')
