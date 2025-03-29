# coding=utf-8

from flask import Request

from api.auth.authenticator import Authenticator
from api.database.entitymanager import EntityManager
from api.database.model.user import User
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import JsonResponse, ErrorJsonResponse


class LoginUser(RequestHandler):

    def __init__(self, authenticator: Authenticator, entity_manager: EntityManager):
        self.authenticator = authenticator
        self.entity_manager = entity_manager

    def handle_request(self, request: Request) -> JsonResponse:
        current_user = self.get_current_identity()

        if current_user:
            return ErrorJsonResponse(f'You are already logged in as {current_user['username']}.', 401)

        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            return ErrorJsonResponse('A username is required.')

        if not password:
            return ErrorJsonResponse('A password is required.')

        if not self.authenticator.authenticate_user(username, password):
            return ErrorJsonResponse('Invalid username or password.', 401)

        user_repository = self.entity_manager.get_repository(User)
        users = user_repository.find_by(username=username)

        access_token = self.authenticator.login_user(username, password)

        return JsonResponse({'success': True, 'access_token': access_token, 'current_user': users[0].to_dictionary()})

    def require_authentication(self) -> bool:
        return False
