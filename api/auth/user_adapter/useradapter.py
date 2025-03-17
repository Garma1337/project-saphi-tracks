# coding: utf-8

from abc import abstractmethod, ABC

from flask_jwt_extended import create_access_token

from api.database.model.user import User


class RegistrationError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class UserAdapter(ABC):

    @abstractmethod
    def authenticate_user(self, username: str, password: str) -> bool:
        pass

    @abstractmethod
    def login_user(self, username: str, password: str) -> User:
        pass

    @abstractmethod
    def register_user(self, username: str, email: str, password: str) -> User:
        pass

    def _create_access_token(self, user: User) -> str:
        return create_access_token(identity = user)
