# coding: utf-8

from datetime import datetime

from api.auth.passwordmanager import PasswordManager
from api.auth.user_adapter.useradapter import AuthenticationError, UserAdapter, RegistrationError
from api.database.entitymanager import EntityManager
from api.database.model.user import User
from api.event.event import Event
from api.event.eventmanager import EventManager
from api.lib.saphiclient import SaphiClient


class SaphiUserAdapter(UserAdapter):

    def __init__(self,
        event_manager: EventManager,
        entity_manager: EntityManager,
        password_manager: PasswordManager,
        saphi_client: SaphiClient
    ):
        self.event_manager = event_manager
        self.entity_manager = entity_manager
        self.password_manager = password_manager
        self.saphi_client = saphi_client

    def authenticate_user(self, username: str, password: str) -> bool:
        response = self.saphi_client.validate_user_credentials(username, password)

        success = bool(response['success'])
        if success:
            self.event_manager.fire_event(Event('saphi_login_successful', {
                'username': username,
                'password': password,
                'user_adapter': self
            }))

        return success

    def login_user(self, username: str, password: str) -> str:
        if not self.authenticate_user(username, password):
            raise AuthenticationError('Invalid username or password.')

        user_repository = self.entity_manager.get_repository(User)
        users = user_repository.find_by(username=username)

        return self._create_access_token(users[0])

    def register_user(self, username: str, email: str, password: str) -> User:
        user_repository = self.entity_manager.get_repository(User)
        users = user_repository.find_by(username=username)

        if len(users) > 0:
            raise RegistrationError(f'A user with the name "{username}" already exists.')

        salt = self.password_manager.generate_salt()
        password = self.password_manager.encode_password(password, salt)

        user = user_repository.create(
            username=username,
            email='',
            password=password,
            salt=salt,
            created=datetime.now(),
            verified=True
        )

        return user
