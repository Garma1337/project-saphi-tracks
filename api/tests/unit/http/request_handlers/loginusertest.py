# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.auth.authenticator import Authenticator
from api.auth.passwordmanager import PasswordManager
from api.auth.user_adapter.localuseradapter import LocalUserAdapter
from api.database.entitymanager import EntityManager
from api.database.model.user import User
from api.http.request_handlers.loginuser import LoginUser
from api.tests.mockmodelrepository import MockModelRepository
from api.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class LoginUserTest(TestCase):

    def setUp(self):
        self.db = SQLAlchemy()
        self.entity_manager = EntityManager(self.db, MockModelRepository)

        self.user_repository = MockModelRepository(self.db, User)
        self.garma = self.user_repository.create(
            username='Garma',
            email='email@domain.com',
            password='Password123!',
            created=datetime.now(),
            verified=True
        )

        self.entity_manager.cache_repository_instance(User, self.user_repository)

        self.password_manager = PasswordManager(MockPasswordEncoderStrategy())

        self.local_user_adapter = LocalUserAdapter(self.entity_manager, self.password_manager)
        self.local_user_adapter._create_access_token = Mock(return_value='123456')

        self.authenticator = Authenticator(self.local_user_adapter)
        self.login_user = LoginUser(self.authenticator, self.entity_manager)

    def test_can_login_user(self):
        self.login_user.get_current_identity = Mock(return_value=None)

        response = self.login_user.handle_request(Request.from_values(json={
            'username': 'Garma',
            'password': 'Password123!'
        }))

        data = response.get_data()
        status_code = response.get_status_code()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['access_token'], '123456')
        self.assertEqual(status_code, 200)

    def test_can_not_login_user_if_already_logged_in(self):
        garma = User()
        garma.username = 'Garma'

        self.login_user.get_current_identity = Mock(return_value=garma.to_dictionary())

        response = self.login_user.handle_request(Request.from_values(json={
            'username': 'Garma',
            'password': 'Password123!'
        }))

        data = response.get_data()
        status_code = response.get_status_code()

        self.assertEqual(data['success'], False)
        self.assertIsNotNone(data['error'])
        self.assertEqual(status_code, 401)

    def test_can_not_login_user_if_no_username(self):
        self.login_user.get_current_identity = Mock(return_value=None)

        response = self.login_user.handle_request(Request.from_values(json={
            'password': 'Password123!'
        }))

        data = response.get_data()
        status_code = response.get_status_code()

        self.assertEqual(data['success'], False)
        self.assertIsNotNone(data['error'])
        self.assertEqual(status_code, 400)

    def test_can_not_login_user_if_no_password(self):
        self.login_user.get_current_identity = Mock(return_value=None)

        response = self.login_user.handle_request(Request.from_values(json={
            'username': 'Garma'
        }))

        data = response.get_data()
        status_code = response.get_status_code()

        self.assertEqual(data['success'], False)
        self.assertIsNotNone(data['error'])
        self.assertEqual(status_code, 400)

    def test_can_not_login_user_if_authentication_fails(self):
        self.login_user.get_current_identity = Mock(return_value=None)

        response = self.login_user.handle_request(Request.from_values(json={
            'username': 'Garma',
            'password': 'password1'
        }))

        data = response.get_data()
        status_code = response.get_status_code()

        self.assertEqual(data['success'], False)
        self.assertIsNotNone(data['error'])
        self.assertEqual(status_code, 401)
