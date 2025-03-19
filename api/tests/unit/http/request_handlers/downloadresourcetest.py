# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.database.entitymanager import EntityManager
from api.database.model.resource import Resource
from api.http.request_handlers.downloadresource import DownloadResource
from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy
from api.resource.file_system_adapter.localfilesystemadapter import LocalFileSystemAdapter
from api.resource.resourcemanager import ResourceManager
from api.tests.mockmodelrepository import MockModelRepository


class DownloadResourceTest(TestCase):

    def setUp(self):
        self.entity_manager = EntityManager(
            SQLAlchemy(),
            MockModelRepository
        )

        self.resource_repository = MockModelRepository(Resource)

        self.file_system_adapter = LocalFileSystemAdapter('.')
        self.file_encoder_strategy = Sha256FileEncoderStrategy()

        self.resource_manager = ResourceManager(
            self.entity_manager,
            self.file_system_adapter,
            self.file_encoder_strategy
        )
        self.resource_manager._send_from_directory = Mock(return_value = None)

        self.permission_resolver = LogicalPermissionResolver()
        self.download_resource = DownloadResource(self.entity_manager, self.resource_manager, self.permission_resolver)
        self.download_resource.get_current_user = Mock(return_value=None)

        self.entity_manager.get_repository = lambda model: self.resource_repository

    def test_can_download_resource(self):
        self.resource_repository.create(
            id=1,
            file_name='file_name',
            verified=True
        )

        response = self.download_resource.handle_request(Request.from_values(query_string='id=1'))

        self.assertEqual(response.status_code, 204)

    def test_can_not_download_resource_when_no_id_specified(self):
        response = self.download_resource.handle_request(Request.from_values(query_string=''))

        self.assertEqual(response.status_code, 400)

    def test_can_not_download_resource_when_resource_does_not_exist(self):
        response = self.download_resource.handle_request(Request.from_values(query_string='id=1'))

        self.assertEqual(response.status_code, 404)

    def test_can_not_download_resource_when_user_does_not_have_permission(self):
        self.resource_repository.create(
            id=1,
            file_name='file_name',
            verified=False
        )

        response = self.download_resource.handle_request(Request.from_values(query_string='id=1'))

        self.assertEqual(response.status_code, 401)
