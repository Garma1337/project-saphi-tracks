# coding: utf-8

from api.auth.passwordmanager import PasswordManager
from api.auth.user_adapter.useradapter import UserAdapter
from api.database.entitymanager import EntityManager
from api.database.model.user import User
from api.event.event import Event
from api.event.eventsubscriber import EventSubscriber


class SaphiLoginSuccessfulEventSubscriber(EventSubscriber):

    def __init__(self, entity_manager: EntityManager, password_manager: PasswordManager):
        self.entity_manager = entity_manager
        self.password_manager = password_manager

    def run_on_event(self, event: Event) -> dict:
        username = event.context['username']
        password = event.context['password']

        user_adapter: UserAdapter = event.context['user_adapter']

        # if the user logs in for the first time, we create a local copy of the user
        # on subsequent logins we just update the user based on the login credentials
        user_repository = self.entity_manager.get_repository(User)
        users = user_repository.find_by(username=username)

        if len(users) <= 0:
            user_adapter.register_user(username, '', password)
        else:
            user = users[0]
            user_repository.update(
                id=user.id,
                username=username,
                password=password,
            )

        return {
            'user_created': len(users) <= 0,
            'user_updated': len(users) > 0,
        }

    def get_event_name(self) -> str:
        return 'saphi_login_successful'

    def get_name(self) -> str:
        return 'saphi_login_successful_event_subscriber'
