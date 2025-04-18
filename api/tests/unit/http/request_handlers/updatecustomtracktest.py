# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.auth.sessionmanager import SessionManager
from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
from api.database.model.permission import Permission
from api.database.model.user import User
from api.http.request_handlers.updatecustomtrack import UpdateCustomTrack
from api.tests.mockmodelrepository import MockModelRepository


class UpdateCustomTrackTest(TestCase):

    def setUp(self):
        self.db = SQLAlchemy()
        self.entity_manager = EntityManager(self.db, MockModelRepository)

        self.custom_track_repository = MockModelRepository(self.db, CustomTrack)
        self.custom_track = self.custom_track_repository.create(
            author_id=1,
            name='Test',
            description='Test description',
            highlighted=False,
            verified=False
        )

        self.user_repository = MockModelRepository(self.db, User)
        self.garma = self.user_repository.create(
            id=1,
            username='Garma',
        )
        self.garma.permission = Permission()
        self.garma.permission.can_edit_custom_tracks = True

        self.entity_manager.cache_repository_instance(CustomTrack, self.custom_track_repository)
        self.entity_manager.cache_repository_instance(User, self.user_repository)

        self.session_manager = SessionManager(self.entity_manager)
        self.permission_resolver = LogicalPermissionResolver()

        self.update_custom_track = UpdateCustomTrack(self.entity_manager, self.session_manager, self.permission_resolver)
        self.update_custom_track.get_current_identity = Mock(return_value=self.garma.to_dictionary())

    def test_can_update_custom_track(self):
        response = self.update_custom_track.handle_request(Request.from_values(json={'id': self.custom_track.id, 'highlighted': True}))
        data = response.get_data()

        self.assertEqual(data['custom_track']['highlighted'], True)

    def test_can_not_update_custom_track_when_no_id_specified(self):
        response = self.update_custom_track.handle_request(Request.from_values(json={}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 400)

    def test_can_not_update_custom_track_when_not_found(self):
        response = self.update_custom_track.handle_request(Request.from_values(json={'id': 2, 'highlighted': True}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 404)

    def test_can_not_update_custom_track_when_user_does_not_have_permission(self):
        self.garma.permission.can_edit_custom_tracks = False

        response = self.update_custom_track.handle_request(Request.from_values(json={'id': self.custom_track.id, 'highlighted': True}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 401)
