# coding: utf-8

from flask import Request

from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse


class GetSession(RequestHandler):

    def handle_request(self, request: Request) -> JsonResponse:
        current_user = self.get_current_user()
        return JsonResponse({'current_user': current_user})

    def require_authentication(self) -> bool:
        return False
