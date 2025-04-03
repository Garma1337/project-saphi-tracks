# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.auth.sessionmanager import SessionManager
from api.database.entitymanager import EntityManager
from api.database.model.permission import Permission
from api.database.model.resource import Resource
from api.database.model.user import User
from api.http.request_handlers.verifyresource import VerifyResource
from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy
from api.resource.resourcemanager import ResourceManager
from api.tests.mockfilesystemadapter import MockFileSystemAdapter
from api.tests.mockmodelrepository import MockModelRepository
from api.util.semvervalidator import SemVerValidator


class VerifyResourceTest(TestCase):

    def setUp(self):
        self.db = SQLAlchemy()
        self.entity_manager = EntityManager(self.db, MockModelRepository)

        self.session_manager = SessionManager(self.entity_manager)

        self.resource_repository = MockModelRepository(self.db, Resource)
        self.resource = self.resource_repository.create(
            author_id=1,
            custom_track_id=1,
            verified=False
        )

        self.user_repository = MockModelRepository(self.db, User)
        self.garma = self.user_repository.create(
            id=1,
            username='Garma',
        )
        self.garma.permission = Permission()
        self.garma.permission.can_edit_resources = True

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

        self.permission_resolver = LogicalPermissionResolver()

        self.verify_resource = VerifyResource(self.session_manager, self.resource_manager, self.permission_resolver)
        self.verify_resource.get_current_identity = Mock(return_value=self.garma.to_dictionary())

    def test_can_verify_resource(self):
        response = self.verify_resource.handle_request(Request.from_values(json={'id': self.resource.id}))
        data = response.get_data()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['resource']['verified'], True)

    def test_can_not_verify_resource_when_no_id_specified(self):
        response = self.verify_resource.handle_request(Request.from_values(json={}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 400)

    def test_can_not_verify_resource_when_user_does_not_have_permission(self):
        self.garma.permission.can_edit_resources = False

        response = self.verify_resource.handle_request(Request.from_values(json={'id': self.resource.id}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 401)

    def test_can_not_verify_resource_when_resource_does_not_exist(self):
        response = self.verify_resource.handle_request(Request.from_values(json={'id': 2}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 404)

    def test_can_not_verify_resource_when_resource_is_already_verified(self):
        self.resource.verified = True

        response = self.verify_resource.handle_request(Request.from_values(json={'id': self.resource.id}))
        status_code = response.get_status_code()

        self.assertEqual(status_code, 400)
