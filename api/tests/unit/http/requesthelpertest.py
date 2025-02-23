# coding: utf-8

from unittest import TestCase

from flask import Request

from api.http.requesthelper import RequestHelper


class RequestHelperTest(TestCase):

    def test_can_get_boolean_query_parameter_from_string(self):
        request = Request.from_values(query_string='test=true')
        self.assertEqual(True, RequestHelper.try_parse_boolean_value(request.args, 'test'))

    def test_can_get_boolean_query_parameter_from_int(self):
        request = Request.from_values(query_string='test=1')
        self.assertEqual(True, RequestHelper.try_parse_boolean_value(request.args, 'test'))

    def test_can_get_boolean_query_parameter_from_false_string(self):
        request = Request.from_values(query_string='test=false')
        self.assertEqual(False, RequestHelper.try_parse_boolean_value(request.args, 'test'))

    def test_can_get_boolean_query_parameter_from_false_int(self):
        request = Request.from_values(query_string='test=0')
        self.assertEqual(False, RequestHelper.try_parse_boolean_value(request.args, 'test'))

    def test_can_get_boolean_query_parameter_from_none(self):
        request = Request.from_values(query_string='test=')
        self.assertIsNone(RequestHelper.try_parse_boolean_value(request.args, 'test'))

    def test_can_get_boolean_query_parameter_from_missing(self):
        request = Request.from_values()
        self.assertIsNone(RequestHelper.try_parse_boolean_value(request.args, 'test'))

    def test_can_get_integer_query_parameter_from_string(self):
        request = Request.from_values(query_string='test=1')
        self.assertEqual(1, RequestHelper.try_parse_integer_value(request.args, 'test'))

    def test_can_get_integer_query_parameter_from_non_number(self):
        request = Request.from_values(query_string='test=abc')
        self.assertIsNone(RequestHelper.try_parse_integer_value(request.args, 'test'))

    def test_can_get_integer_query_parameter_from_none(self):
        request = Request.from_values(query_string='test=')
        self.assertIsNone(RequestHelper.try_parse_integer_value(request.args, 'test'))

    def test_can_get_integer_query_parameter_from_missing(self):
        request = Request.from_values()
        self.assertIsNone(RequestHelper.try_parse_integer_value(request.args, 'test'))
