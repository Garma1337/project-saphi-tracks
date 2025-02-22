# coding=utf-8

from flask import Request

from api.http.response import ErrorJsonResponse, JsonResponse
from api.http.router import Router


class DispatcherErrror(Exception):
    pass


class Dispatcher(object):

    def __init__(self, router: Router) -> None:
        self.router = router

    def dispatch_request(self, requested_route: str, request: Request) -> JsonResponse:
        if not requested_route:
            return ErrorJsonResponse('No route specified', 400)

        if not self.router.has_request_handler(requested_route, request.method):
            return ErrorJsonResponse(f'No route /{requested_route} exists', 404)

        request_handler = self.router.get_request_handler_for_route(requested_route, request.method)

        if request_handler.require_authentication():
            try:
                request_handler.assert_user_is_authenticated()
            except ValueError as e:
                return ErrorJsonResponse(str(e), 401)

        return request_handler.handle_request(request)
