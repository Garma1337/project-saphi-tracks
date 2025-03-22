# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.database.entitymanager import EntityManager
from api.database.model.permission import Permission
from api.database.model.resource import Resource, ResourceType
from api.database.model.user import User
from api.http.request_handlers.verifyresource import VerifyResource
from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy
from api.resource.resourcemanager import ResourceManager
from api.tests.mockfilesystemadapter import MockFileSystemAdapter
from api.tests.mockmodelrepository import MockModelRepository


class VerifyResourceTest(TestCase):

    def setUp(self):
        self.entity_manager = EntityManager(SQLAlchemy(), MockModelRepository)

        self.resource_repository = MockModelRepository(Resource)
        self.resource = self.resource_repository.create(
            author_id=1,
            custom_track_id=1,
            verified=False
        )

        self.entity_manager.get_repository = lambda model: self.resource_repository

        self.file_system_adapter = MockFileSystemAdapter()
        self.file_encoder_strategy = Sha256FileEncoderStrategy()

        self.resource_manager = ResourceManager(
            self.entity_manager,
            self.file_system_adapter,
            self.file_encoder_strategy
        )

        self.permission_resolver = LogicalPermissionResolver()

        self.garma = User()
        self.garma.permission = Permission()
        self.garma.permission.can_edit_resources = True

        self.verify_resource = VerifyResource(self.resource_manager, self.permission_resolver)
        self.verify_resource.get_current_user = Mock(return_value=self.garma)

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
