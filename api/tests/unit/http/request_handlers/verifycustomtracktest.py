# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
from api.database.model.permission import Permission
from api.database.model.resource import Resource
from api.database.model.user import User
from api.http.request_handlers.verifycustomtrack import VerifyCustomTrack
from api.lib.customtrackmanager import CustomTrackManager
from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy
from api.resource.resourcemanager import ResourceManager
from api.tests.mockfilesystemadapter import MockFileSystemAdapter
from api.tests.mockmodelrepository import MockModelRepository


class VerifyCustomTrackTest(TestCase):

    def setUp(self):
        self.entity_manager = EntityManager(SQLAlchemy(), MockModelRepository)

        self.custom_track_repository = MockModelRepository(CustomTrack)
        self.custom_track = self.custom_track_repository.create(
            author_id=1,
            verified=False
        )

        self.resource_repository = MockModelRepository(Resource)
        self.entity_manager.get_repository = lambda model: self.custom_track_repository if model == CustomTrack else self.resource_repository

        self.file_system_adapter = MockFileSystemAdapter()
        self.file_encoder_strategy = Sha256FileEncoderStrategy()

        self.resource_manager = ResourceManager(
            self.entity_manager,
            self.file_system_adapter,
            self.file_encoder_strategy
        )

        self.custom_track_manager = CustomTrackManager(
            self.entity_manager,
            self.resource_manager
        )

        self.permission_resolver = LogicalPermissionResolver()

        self.garma = User()
        self.garma.permission = Permission()
        self.garma.permission.can_edit_custom_tracks = True

        self.verify_custom_track = VerifyCustomTrack(self.custom_track_manager, self.permission_resolver)
        self.verify_custom_track.get_current_user = Mock(return_value=self.garma)

    def test_can_verify_custom_track(self):
        response = self.verify_custom_track.handle_request(Request.from_values(json={'id': self.custom_track.id}))
        data = response.get_data()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['custom_track']['verified'], True)

    def test_can_not_verify_custom_track_when_no_id_specified(self):
        response = self.verify_custom_track.handle_request(Request.from_values(json={}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 400)

    def test_can_not_verify_custom_track_when_custom_track_does_not_exist(self):
        response = self.verify_custom_track.handle_request(Request.from_values(json={'id': 2}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 404)

    def test_can_not_verify_custom_track_when_user_does_not_have_permission(self):
        self.garma.permission.can_edit_custom_tracks = False

        response = self.verify_custom_track.handle_request(Request.from_values(json={'id': self.custom_track.id}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 401)

    def test_can_not_verify_custom_track_when_custom_track_is_already_verified(self):
        self.custom_track_repository.update(id=self.custom_track.id, verified=True)

        response = self.verify_custom_track.handle_request(Request.from_values(json={'id': self.custom_track.id}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 400)
