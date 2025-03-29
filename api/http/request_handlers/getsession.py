# coding: utf-8

from flask import Request

from api.auth.sessionmanager import SessionManager
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse
from api.ui.displayoptionsgenerator import DisplayOptionsGenerator


class GetSession(RequestHandler):

    def __init__(self, session_manager: SessionManager, display_options_generator: DisplayOptionsGenerator):
        self.session_manager = session_manager
        self.display_options_generator = display_options_generator

    def handle_request(self, request: Request) -> JsonResponse:
        current_user = self.session_manager.find_user_by_jwt_identity(self.get_current_identity())

        return JsonResponse({
            'current_user': current_user.to_dictionary() if current_user else None,
            'display_options': self.display_options_generator.generate_display_options_for_user(current_user)
        })

    def require_authentication(self) -> bool:
        return False
