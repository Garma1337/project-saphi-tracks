# coding=utf-8

from api.auth.user_adapter.useradapter import UserAdapter
from api.database.model.user import User


class Authenticator(object):

    def __init__(self, user_adapter: UserAdapter):
        self.user_adapter = user_adapter

    def authenticate_user(self, username: str, password: str) -> bool:
        return self.user_adapter.authenticate_user(username, password)

    def login_user(self, username: str, password: str) -> User:
        return self.user_adapter.login_user(username, password)

    def register_user(self, username: str, email: str, password: str) -> User:
        return self.user_adapter.register_user(username, email, password)
