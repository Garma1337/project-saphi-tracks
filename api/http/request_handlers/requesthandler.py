# coding: utf-8

from abc import abstractmethod, ABC

from flask import Request
from flask_jwt_extended import get_jwt_identity

from api.database.model.user import User
from api.http.response import JsonResponse


class RequestHandler(ABC):

    @abstractmethod
    def handle_request(self, request: Request) -> JsonResponse:
        pass

    @abstractmethod
    def require_authentication(self) -> bool:
        pass

    def assert_user_is_authenticated(self):
        if not self.get_current_user():
            raise ValueError('You need to be authenticated to perform this action.')

    def get_current_user(self) -> User:
        return get_jwt_identity()
