# coding: utf-8

from datetime import datetime

from api.auth.passwordmanager import PasswordManager
from api.auth.user_adapter.useradapter import UserAdapter, AuthenticationError, RegistrationError
from api.database.entitymanager import EntityManager
from api.database.model.permission import Permission
from api.database.model.user import User


class LocalUserAdapter(UserAdapter):

    def __init__(self, entity_manager: EntityManager, password_manager: PasswordManager):
        self.entity_manager = entity_manager
        self.password_manager = password_manager

    def authenticate_user(self, username: str, password: str) -> bool:
        user_repository = self.entity_manager.get_repository(User)
        users = user_repository.find_by(username=username)

        if len(users) <= 0:
            return False

        user = users[0]

        if not self.password_manager.check_password(password, user.password, user.salt):
            return False

        return True

    def login_user(self, username: str, password: str) -> str:
        if not self.authenticate_user(username, password):
            raise AuthenticationError('Invalid username or password.')

        user_repository = self.entity_manager.get_repository(User)
        users = user_repository.find_by(username=username)

        return self._create_access_token(users[0])

    def register_user(self, username: str, email: str, password: str) -> User:
        user_repository = self.entity_manager.get_repository(User)
        existing_users = user_repository.find_by(username=username)

        if len(existing_users) > 0:
            raise RegistrationError(f'A user with the name "{username}" already exists.')

        existing_users = user_repository.find_by(email=email)

        if len(existing_users) > 0:
            raise RegistrationError(f'The e-mail address "{email}" is already in use.')

        if not self.password_manager.is_secure_password(password):
            raise RegistrationError('The provided password is not secure enough.')

        salt = self.password_manager.generate_salt()
        encoded_password = self.password_manager.encode_password(password, salt)

        user = user_repository.create(
            username=username,
            email=email,
            password=encoded_password,
            salt=salt,
            created=datetime.now(),
            verified=False
        )

        permission_repository = self.entity_manager.get_repository(Permission)
        permission_repository.create(
            user_id=user.id,
            can_edit_custom_tracks=False,
            can_delete_custom_tracks=False,
            can_edit_resources=False,
            can_delete_resources=False,
            can_edit_users=False
        )

        return user
