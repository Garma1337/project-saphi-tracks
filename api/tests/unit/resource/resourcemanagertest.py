# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask_sqlalchemy import SQLAlchemy

from api.database.entitymanager import EntityManager
from api.database.model.resource import Resource
from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy
from api.resource.file_system_adapter.localfilesystemadapter import LocalFileSystemAdapter
from api.resource.resourcemanager import ResourceManager
from api.tests.mockmodelrepository import MockModelRepository


class ResourceManagerTest(TestCase):

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

        self.entity_manager.get_repository = lambda model: self.resource_repository

    def test_can_get_expected_file_extensions(self):
        self.assertEqual(['jpg', 'png'], self.resource_manager.get_expected_file_extensions('preview'))
        self.assertEqual(['xdelta'], self.resource_manager.get_expected_file_extensions('xdelta'))
        self.assertEqual(['vrm'], self.resource_manager.get_expected_file_extensions('vrm'))
        self.assertEqual(['lev'], self.resource_manager.get_expected_file_extensions('lev'))

    def test_can_not_get_expected_file_extensions_for_non_existent_resource_type(self):
        with self.assertRaises(KeyError):
            self.resource_manager.get_expected_file_extensions('non_existent_resource_type')

    def test_can_offer_resource_download(self):
        self.resource_repository.create(
            id=1,
            file_name='file_name'
        )

        self.resource_manager.offer_resource_download(1)

    def test_can_not_offer_resource_download_for_non_existent_resource(self):
        with self.assertRaises(ValueError):
            self.resource_manager.offer_resource_download(1)
