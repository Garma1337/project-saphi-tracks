# coding: utf-8

from flask import Request

from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse


class CreateCustomTrack(RequestHandler):

    def handle_request(self, request: Request) -> JsonResponse:
        pass

    def require_authentication(self) -> bool:
        return True
