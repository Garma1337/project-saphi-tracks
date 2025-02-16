# coding: utf-8

from unittest import TestCase

from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import Response
from api.http.router import Router


class TestRequestHandler(RequestHandler):

    def handle_request(self, request):
        return Response({ 'test': 'test' })

    def require_authentication(self):
        return False


class RouterTest(TestCase):

    def setUp(self):
        self.router = Router()
        self.test_request_handler = TestRequestHandler()

    def test_can_add_route(self):
        self.router.add_route('test', 'GET', self.test_request_handler)
        self.assertTrue(self.router.has_request_handler('test', 'GET'))

    def test_can_add_route_twice_with_different_methods(self):
        self.router.add_route('test', 'GET', self.test_request_handler)
        self.router.add_route('test', 'POST', self.test_request_handler)

        self.assertTrue(self.router.has_request_handler('test', 'GET'))
        self.assertTrue(self.router.has_request_handler('test', 'POST'))

    def test_can_not_add_route_twice_with_same_method(self):
        self.router.add_route('test', 'GET', self.test_request_handler)

        with self.assertRaises(ValueError):
            self.router.add_route('test', 'GET', self.test_request_handler)

    def test_can_get_request_handler_for_route(self):
        self.router.add_route('test', 'GET', self.test_request_handler)
        self.assertEqual(self.test_request_handler, self.router.get_request_handler_for_route('test', 'GET'))

    def test_can_not_get_request_handler_for_non_existent_route(self):
        self.assertIsNone(self.router.get_request_handler_for_route('test', 'GET'))

    def test_can_not_get_request_handler_for_non_existent_method(self):
        self.router.add_route('test', 'GET', self.test_request_handler)
        self.assertIsNone(self.router.get_request_handler_for_route('test', 'POST'))

    def test_can_check_if_route_has_request_handler(self):
        self.router.add_route('test', 'GET', self.test_request_handler)
        self.assertTrue(self.router.has_request_handler('test', 'GET'))

    def test_can_check_if_route_has_no_request_handler(self):
        self.assertFalse(self.router.has_request_handler('test', 'GET'))

    def test_can_remove_route(self):
        self.router.add_route('test', 'GET', self.test_request_handler)
        self.router.remove_route('test', 'GET')
        self.assertFalse(self.router.has_request_handler('test', 'GET'))

    def test_can_not_remove_non_existent_route(self):
        self.router.remove_route('test', 'GET')
        self.assertFalse(self.router.has_request_handler('test', 'GET'))

    def test_can_not_remove_non_existent_method(self):
        self.router.add_route('test', 'GET', self.test_request_handler)
        self.router.remove_route('test', 'POST')

        self.assertTrue(self.router.has_request_handler('test', 'GET'))
        self.assertFalse(self.router.has_request_handler('test', 'POST'))
