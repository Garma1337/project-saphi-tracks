# coding: utf-8

from unittest import TestCase

from flask_sqlalchemy import SQLAlchemy

from api.auth.sessionmanager import SessionManager
from api.database.entitymanager import EntityManager
from api.database.model.user import User
from api.tests.mockmodelrepository import MockModelRepository


class SessionManagerTest(TestCase):

    def setUp(self):
        self.db = SQLAlchemy()
        self.entity_manager = EntityManager(self.db, MockModelRepository)

        self.user_repository = MockModelRepository(self.db, User)
        self.garma = self.user_repository.create(
            id=1,
            username='Garma',
        )

        self.entity_manager.cache_repository_instance(User, self.user_repository)

        self.session_manager = SessionManager(self.entity_manager)

    def test_can_find_user_by_current_identity(self):
        current_user = self.session_manager.find_user_by_jwt_identity({'id': 1, 'username': 'Garma'})
        self.assertEqual(current_user, self.garma)

    def test_can_not_find_user_if_identity_is_none(self):
        current_user = self.session_manager.find_user_by_jwt_identity(None)
        self.assertIsNone(current_user)
