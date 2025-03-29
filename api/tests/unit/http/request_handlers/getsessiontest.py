# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.auth.sessionmanager import SessionManager
from api.database.entitymanager import EntityManager
from api.database.model.user import User
from api.http.request_handlers.getsession import GetSession
from api.tests.mockmodelrepository import MockModelRepository
from api.ui.displayoptionsgenerator import DisplayOptionsGenerator


class GetSessionTest(TestCase):

    def setUp(self):
        self.entity_manager = EntityManager(SQLAlchemy(), MockModelRepository)
        self.session_manager = SessionManager(self.entity_manager)

        self.permission_resolver = LogicalPermissionResolver()
        self.display_options_generator = DisplayOptionsGenerator(self.permission_resolver)

        self.user_repository = MockModelRepository(User)
        self.garma = self.user_repository.create(
            id=1,
            username='Garma',
        )

        self.get_session = GetSession(self.session_manager, self.display_options_generator)
        self.entity_manager.get_repository = lambda model: self.user_repository

    def test_can_get_session_if_logged_in(self):
        self.permission_resolver.can_verify_custom_track = Mock(return_value=False)
        self.get_session.get_current_identity = Mock(return_value=self.garma.to_dictionary())

        response = self.get_session.handle_request(Request.from_values())
        data = response.get_data()

        self.assertEqual(data['current_user'], self.garma.to_dictionary())
        self.assertTrue('display_options' in data)

    def test_can_get_session_if_not_logged_in(self):
        self.permission_resolver.can_verify_custom_track = Mock(return_value=False)
        self.get_session.get_current_identity = Mock(return_value=None)

        response = self.get_session.handle_request(Request.from_values())
        data = response.get_data()

        self.assertEqual(data['current_user'], None)
        self.assertTrue('display_options' in data)
