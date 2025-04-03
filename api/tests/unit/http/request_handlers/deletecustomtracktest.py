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
from api.database.model.resource import Resource
from api.database.model.user import User
from api.http.request_handlers.deletecustomtrack import DeleteCustomTrack
from api.lib.customtrackmanager import CustomTrackManager
from api.lib.semvervalidator import SemVerValidator
from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy
from api.resource.resourcemanager import ResourceManager
from api.tests.mockfilesystemadapter import MockFileSystemAdapter
from api.tests.mockmodelrepository import MockModelRepository


class DeleteCustomTrackTest(TestCase):

    def setUp(self):
        self.db = SQLAlchemy()
        self.entity_manager = EntityManager(self.db, MockModelRepository)
        self.session_manager = SessionManager(self.entity_manager)

        self.custom_track_repository = MockModelRepository(self.db, CustomTrack)
        self.custom_track = self.custom_track_repository.create(
            id=1,
            author_id=1,
            name='Test Custom Track',
            description='This is a test custom track',
            highlighted=False,
            verified=True
        )

        self.resource_repository = MockModelRepository(self.db, Resource)
        self.resource = self.resource_repository.create(
            id=1,
            author_id=1,
            custom_track_id=self.custom_track.id,
            file_name='preview.png',
            verified=True
        )

        self.custom_track.resources = [self.resource]

        self.user_repository = MockModelRepository(self.db, User)
        self.garma = self.user_repository.create(
            id=1,
            username='Garma',
        )

        self.garma.permission = Permission()
        self.garma.permission.can_edit_custom_tracks = True

        self.entity_manager.cache_repository_instance(CustomTrack, self.custom_track_repository)
        self.entity_manager.cache_repository_instance(Resource, self.resource_repository)
        self.entity_manager.cache_repository_instance(User, self.user_repository)

        self.file_system_adapter = MockFileSystemAdapter()
        self.file_encoder_strategy = Sha256FileEncoderStrategy()
        self.semver_validator = SemVerValidator()

        self.resource_manager = ResourceManager(
            self.entity_manager,
            self.file_system_adapter,
            self.file_encoder_strategy,
            self.semver_validator
        )

        self.custom_track_manager = CustomTrackManager(
            self.entity_manager,
            self.resource_manager
        )

        self.permission_resolver = LogicalPermissionResolver()
        self.delete_custom_track = DeleteCustomTrack(
            self.session_manager,
            self.custom_track_manager,
            self.permission_resolver
        )

        self.delete_custom_track.get_current_identity = Mock(return_value=self.garma.to_dictionary())

    def test_can_delete_custom_track(self):
        response = self.delete_custom_track.handle_request(Request.from_values(json={'id': self.custom_track.id}))
        data = response.get_data()

        custom_track = self.custom_track_repository.find_one(self.custom_track.id)
        resource = self.resource_repository.find_one(self.resource.id)

        self.assertEqual(data['success'], True)
        self.assertEqual(custom_track, None)
        self.assertEqual(resource, None)

    def test_can_not_delete_custom_track_when_no_id_specified(self):
        response = self.delete_custom_track.handle_request(Request.from_values(json={}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 400)

    def test_can_not_delete_custom_track_when_id_is_empty(self):
        response = self.delete_custom_track.handle_request(Request.from_values(json={'id': ''}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 404)

    def test_can_not_delete_custom_track_when_user_does_not_have_permission(self):
        self.garma.permission.can_edit_custom_tracks = False

        response = self.delete_custom_track.handle_request(Request.from_values(json={'id': self.custom_track.id}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 401)

    def test_can_not_delete_custom_track_when_custom_track_does_not_exist(self):
        response = self.delete_custom_track.handle_request(Request.from_values(json={'id': 2}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 404)
