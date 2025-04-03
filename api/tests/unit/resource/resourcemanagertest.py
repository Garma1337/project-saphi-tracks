# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage

from api.database.entitymanager import EntityManager
from api.database.model.resource import Resource, ResourceType
from api.database.model.user import User
from api.lib.semvervalidator import SemVerValidator
from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy
from api.resource.resourcemanager import ResourceManager, ResourceNotFoundError, ResourceAlreadyVerifiedError, \
    ResourceCreationError
from api.tests.mockfilesystemadapter import MockFileSystemAdapter
from api.tests.mockmodelrepository import MockModelRepository


class ResourceManagerTest(TestCase):

    def setUp(self):
        self.db = SQLAlchemy()

        self.entity_manager = EntityManager(
            SQLAlchemy(),
            MockModelRepository
        )

        self.resource_repository = MockModelRepository(self.db, Resource)
        self.user_repository = MockModelRepository(self.db, User)
        self.garma = self.user_repository.create(
            id=1,
            username='Garma',
        )

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

        self.resource_manager._get_current_ts = Mock(return_value=123456789)

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

    def test_can_create_resource_from_uploaded_file(self):
        resource = self.resource_manager.create_resource_from_uploaded_file(
            self.garma.id,
            ResourceType.PREVIEW.value,
            FileStorage(filename='greenhill_zone.jpg', content_type='image/jpeg', content_length=1024),
            '1.0.0'
        )

        self.assertTrue(self.file_system_adapter.file_exists(resource.file_name))
        self.assertEqual('123456789_preview.jpg', resource.file_name)
        self.assertEqual(1024, resource.file_size)

    def test_can_not_create_resource_from_uploaded_file_with_invalid_user(self):
        with self.assertRaises(ResourceCreationError):
            self.resource_manager.create_resource_from_uploaded_file(
                999,
                ResourceType.PREVIEW.value,
                FileStorage(filename='greenhill_zone.jpg', content_type='image/jpeg', content_length=1024),
                '1.0.0'
            )

    def test_can_not_create_resource_from_uploaded_file_with_invalid_version(self):
        with self.assertRaises(ResourceCreationError):
            self.resource_manager.create_resource_from_uploaded_file(
                self.garma.id,
                ResourceType.PREVIEW.value,
                FileStorage(filename='greenhill_zone.jpg', content_type='image/jpeg', content_length=1024),
                'invalid_version'
            )

    def test_can_not_create_resource_from_uploaded_file_with_large_file(self):
        with self.assertRaises(ResourceCreationError):
            self.resource_manager.create_resource_from_uploaded_file(
                self.garma.id,
                ResourceType.PREVIEW.value,
                FileStorage(filename='greenhill_zone.jpg', content_type='image/jpeg', content_length=1024 * 1024 * 11),
                '1.0.0'
            )

    def test_can_not_create_resource_from_uploaded_file_with_invalid_file_extension(self):
        with self.assertRaises(ResourceCreationError):
            self.resource_manager.create_resource_from_uploaded_file(
                self.garma.id,
                ResourceType.PREVIEW.value,
                FileStorage(filename='greenhill_zone.txt', content_type='text/plain', content_length=1024),
                '1.0.0'
            )

    def test_can_not_create_resource_from_uploaded_file_with_invalid_mime_type(self):
        with self.assertRaises(ResourceCreationError):
            self.resource_manager.create_resource_from_uploaded_file(
                self.garma.id,
                ResourceType.PREVIEW.value,
                FileStorage(filename='greenhill_zone.jpg', content_type='text/plain', content_length=1024),
                '1.0.0'
            )

    def test_can_move_uploaded_file(self):
        uploaded_file = FileStorage(filename='greenhill_zone.jpg', content_type='image/jpeg', content_length=1024)
        destination_file_name = 'destination_file_name.jpg'

        file_path = self.resource_manager.move_uploaded_file(uploaded_file, destination_file_name)

        self.assertTrue(self.file_system_adapter.file_exists(destination_file_name))
        self.assertEqual('8d/1c/c9/destination_file_name.jpg', str(file_path))

    def test_can_verify_resource(self):
        resource = self.resource_repository.create(
            id=1,
            file_name='file_name'
        )

        verified_resource = self.resource_manager.verify_resource(resource.id)

        self.assertEqual(1, verified_resource.id)
        self.assertEqual(True, verified_resource.verified)

    def test_can_not_verify_non_existent_resource(self):
        with self.assertRaises(ResourceNotFoundError):
            self.resource_manager.verify_resource(1)

    def test_can_not_verify_already_verified_resource(self):
        resource = self.resource_repository.create(
            id=1,
            file_name='file_name',
            verified=True
        )

        with self.assertRaises(ResourceAlreadyVerifiedError):
            self.resource_manager.verify_resource(resource.id)

    def test_can_generate_file_name_for_resource_type(self):
        self.assertEqual('preview', self.resource_manager.generate_file_name_for_resource_type(ResourceType.PREVIEW.value))
        self.assertEqual('patch', self.resource_manager.generate_file_name_for_resource_type(ResourceType.XDELTA.value))
        self.assertEqual('texture', self.resource_manager.generate_file_name_for_resource_type(ResourceType.VRM.value))
        self.assertEqual('level', self.resource_manager.generate_file_name_for_resource_type(ResourceType.LEV.value))

    def test_can_not_generate_file_name_for_non_existent_resource_type(self):
        with self.assertRaises(KeyError):
            self.resource_manager.generate_file_name_for_resource_type('non_existent_resource_type')
