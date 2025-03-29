# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask_sqlalchemy import SQLAlchemy

from api.auth.passwordmanager import PasswordManager
from api.auth.user_adapter.saphiuseradapter import SaphiUserAdapter
from api.auth.user_adapter.useradapter import AuthenticationError, RegistrationError
from api.database.entitymanager import EntityManager
from api.database.model.permission import Permission
from api.database.model.user import User
from api.event.eventmanager import EventManager
from api.event.subscribers.saphiloginsuccessfuleventsubscriber import SaphiLoginSuccessfulEventSubscriber
from api.lib.saphiclient import SaphiClient
from api.tests.mockmodelrepository import MockModelRepository
from api.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class SaphiUserAdapterTest(TestCase):

    def setUp(self):
        self.db = SQLAlchemy()

        self.entity_manager = EntityManager(self.db, MockModelRepository)
        self.password_manager = PasswordManager(MockPasswordEncoderStrategy())

        self.user_repository = MockModelRepository(User)
        self.permission_repository = MockModelRepository(Permission)

        repositories = {
            Permission: self.permission_repository,
            User: self.user_repository
        }

        self.event_manager = EventManager()
        self.event_manager.register_event_subscriber(SaphiLoginSuccessfulEventSubscriber(self.entity_manager, self.password_manager))

        self.saphi_client = SaphiClient('http://127.0.0.1/api', '123456')

        self.saphi_user_adapter = SaphiUserAdapter(
            self.event_manager,
            self.entity_manager,
            self.password_manager,
            self.saphi_client
        )

        self.entity_manager.get_repository = lambda model: repositories[model]

    def test_can_authenticate_user(self):
        self.saphi_client.validate_user_credentials = Mock(return_value={'success': True})

        self.assertTrue(self.saphi_user_adapter.authenticate_user('Garma', 'Password123!'))
        self.assertEqual(len(self.user_repository.find_by(username='Garma')), 1)

    def test_can_not_authenticate_user_if_wrong_password(self):
        self.saphi_client.validate_user_credentials = Mock(return_value={'success': False})

        self.assertFalse(self.saphi_user_adapter.authenticate_user('Garma', 'password1'))
        self.assertEqual(len(self.user_repository.find_by(username='Garma')), 0)

    def test_can_login_user(self):
        self.saphi_client.validate_user_credentials = Mock(return_value={'success': True})
        self.saphi_user_adapter._create_access_token = Mock(return_value='123456')

        token = self.saphi_user_adapter.login_user('Garma', 'Password123!')
        self.assertEqual('123456', token)

    def test_can_not_login_user_if_wrong_password(self):
        self.saphi_client.validate_user_credentials = Mock(return_value={'success': False})

        with self.assertRaises(AuthenticationError):
            self.saphi_user_adapter.login_user('Garma', 'password1')

    def test_can_register_user(self):
        player = self.saphi_user_adapter.register_user('Dutchesss', '', 'test123456')
        self.assertIsNotNone(player)

    def test_can_not_register_user_if_username_already_exists(self):
        self.saphi_user_adapter.register_user('Garma', '', 'password1')

        with self.assertRaises(RegistrationError):
            self.saphi_user_adapter.register_user('Garma', '', 'password1')
