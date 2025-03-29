# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from flask_sqlalchemy import SQLAlchemy

from api.auth.passwordmanager import PasswordManager
from api.auth.user_adapter.localuseradapter import LocalUserAdapter
from api.auth.user_adapter.useradapter import RegistrationError, AuthenticationError
from api.database.entitymanager import EntityManager
from api.database.model.permission import Permission
from api.database.model.user import User
from api.tests.mockmodelrepository import MockModelRepository
from api.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class LocalUserAdapterTest(TestCase):

    def setUp(self):
        self.db = SQLAlchemy()

        self.entity_manager = EntityManager(self.db, MockModelRepository)
        self.password_manager = PasswordManager(MockPasswordEncoderStrategy())

        self.user_repository = MockModelRepository(User)
        self.garma = self.user_repository.create(
            username='Garma',
            email='email@domain.com',
            password='Password123!',
            salt='123456',
            created=datetime.now(),
            verified=True
        )

        self.permission_repository = MockModelRepository(Permission)

        repositories = {
            Permission: self.permission_repository,
            User: self.user_repository
        }

        self.local_user_adapter = LocalUserAdapter(
            self.entity_manager,
            self.password_manager
        )

        self.local_user_adapter.entity_manager.get_repository = lambda model: repositories[model]

    def test_can_authenticate_user(self):
        self.assertTrue(self.local_user_adapter.authenticate_user('Garma', 'Password123!'))

    def test_can_not_authenticate_user_if_wrong_password(self):
        self.assertFalse(self.local_user_adapter.authenticate_user('Garma', 'password1'))

    def test_can_not_authenticate_user_if_wrong_username(self):
        self.assertFalse(self.local_user_adapter.authenticate_user('Garma1', 'password'))

    def test_can_not_authenticate_user_if_wrong_username_and_password(self):
        self.assertFalse(self.local_user_adapter.authenticate_user('Garma1', 'password1'))

    def test_can_login_user(self):
        self.local_user_adapter._create_access_token = Mock(return_value='123456')

        token = self.local_user_adapter.login_user('Garma', 'Password123!')
        self.assertEqual('123456', token)

    def test_can_not_login_user_if_wrong_password(self):
        with self.assertRaises(AuthenticationError):
            self.local_user_adapter.login_user('Garma', 'password1')

    def test_can_register_user(self):
        player = self.local_user_adapter.register_user('Dutchesss', 'email2@domain2.com', 'ruheoiI"1122"!#xx')
        self.assertIsNotNone(player)

    def test_can_not_register_user_if_username_already_exists(self):
        with self.assertRaises(RegistrationError):
            self.local_user_adapter.register_user('Garma', 'email2@domain2.com', 'ruheoiI"1122"!#xx')

    def test_can_not_register_user_if_email_already_exists(self):
        with self.assertRaises(RegistrationError):
            self.local_user_adapter.register_user('Dutchesss', 'email@domain.com', 'ruheoiI"1122"!#xx')

    def test_can_not_register_user_if_password_is_not_secure(self):
        with self.assertRaises(RegistrationError):
            self.local_user_adapter.register_user('Dutchesss', 'email2@domain2.com', 'password')
