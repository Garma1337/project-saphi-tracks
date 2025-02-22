# coding: utf-8

from unittest import TestCase

from flask import Request

from api.http.dispatcher import Dispatcher
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse
from api.http.router import Router
from unit.http.routertest import TestRequestHandler


class AuthenticationRequiredRequestHandler(RequestHandler):

    def handle_request(self, request: Request):
        return JsonResponse({'test': 'test'})

    def require_authentication(self):
        return True

    def assert_user_is_authenticated(self):
        raise ValueError('You need to be authenticated to perform this action.')


class DispatcherTest(TestCase):

    def setUp(self):
        self.router = Router()
        self.router.add_route('test', 'GET', TestRequestHandler())

        self.dispatcher = Dispatcher(self.router)

    def test_can_dispatch_request(self):
        response = self.dispatcher.dispatch_request('test', Request.from_values())

        self.assertEqual(200, response.get_status_code())
        self.assertEqual({'test': 'test'}, response.get_data())

    def test_can_not_dispatch_request_with_no_route(self):
        response = self.dispatcher.dispatch_request('', Request.from_values())
        self.assertEqual(400, response.get_status_code())

    def test_can_not_dispatch_request_with_no_route_handler(self):
        response = self.dispatcher.dispatch_request('non_existent_route', Request.from_values())
        self.assertEqual(404, response.get_status_code())

    def test_can_not_dispatch_request_with_unauthenticated_request(self):
        self.router.add_route('test2', 'GET', AuthenticationRequiredRequestHandler())

        response = self.dispatcher.dispatch_request('test2', Request.from_values())
        self.assertEqual(401, response.get_status_code())

    def test_can_dispatch_request_with_authenticated_request(self):
        request_handler = AuthenticationRequiredRequestHandler()
        request_handler.assert_user_is_authenticated = lambda: None

        self.router.add_route('test2', 'GET', request_handler)

        response = self.dispatcher.dispatch_request('test2', Request.from_values())
        self.assertEqual(200, response.get_status_code())
