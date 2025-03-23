# coding: utf-8

from flask import Request

from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse, SuccessJsonResponse, ErrorJsonResponse


class CreateCustomTrack(RequestHandler):

    def handle_request(self, request: Request) -> JsonResponse:
        print("Files Received:", request.files)
        print("Data Received:", request.form)

        return SuccessJsonResponse({'custom_track': {}})

    def require_authentication(self) -> bool:
        return True
