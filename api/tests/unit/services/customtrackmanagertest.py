# coding: utf-8

from unittest import TestCase

from flask_sqlalchemy import SQLAlchemy

from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
from api.database.model.resource import Resource
from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy
from api.resource.resourcemanager import ResourceManager
from api.services.customtrackmanager import CustomTrackManager, CustomTrackNotFoundError, \
    CustomTrackAlreadyVerifiedError
from api.tests.mockfilesystemadapter import MockFileSystemAdapter
from api.tests.mockmodelrepository import MockModelRepository
from api.util.semvervalidator import SemVerValidator


class CustomTrackManagerTest(TestCase):

    def setUp(self):
        self.db = SQLAlchemy()
        self.entity_manager = EntityManager(self.db, MockModelRepository)

        self.custom_track_repository = MockModelRepository(self.db, CustomTrack)
        self.resource_repository = MockModelRepository(self.db, Resource)

        self.entity_manager.cache_repository_instance(CustomTrack, self.custom_track_repository)
        self.entity_manager.cache_repository_instance(Resource, self.resource_repository)

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

    def test_can_verify_custom_track(self):
        custom_track = self.custom_track_repository.create(
            author_id=1,
            verified=False
        )

        custom_track.resources = [
            self.resource_repository.create(
                author_id=1,
                custom_track_id=custom_track.id,
                verified=False
            )
        ]

        self.custom_track_manager.verify_custom_track(custom_track.id)

        self.assertTrue(custom_track.verified)
        self.assertTrue(all(resource.verified for resource in custom_track.resources))

    def test_can_not_verify_custom_track_when_not_found(self):
        with self.assertRaises(CustomTrackNotFoundError):
            self.custom_track_manager.verify_custom_track(1)

    def test_can_not_verify_custom_track_when_already_verified(self):
        custom_track = self.custom_track_repository.create(
            author_id=1,
            verified=True
        )

        with self.assertRaises(CustomTrackAlreadyVerifiedError):
            self.custom_track_manager.verify_custom_track(custom_track.id)

    def test_can_delete_custom_track(self):
        custom_track = self.custom_track_repository.create(
            author_id=1,
            verified=False
        )

        resource = self.resource_repository.create(
            author_id=1,
            file_name='preview.png',
            custom_track_id=custom_track.id,
            verified=False
        )

        custom_track.resources = [resource]

        self.custom_track_manager.delete_custom_track(custom_track.id)

        self.assertIsNone(self.custom_track_repository.find_one(custom_track.id))
        self.assertIsNone(self.resource_repository.find_one(resource.id))

    def test_can_not_delete_custom_track_when_not_found(self):
        with self.assertRaises(CustomTrackNotFoundError):
            self.custom_track_manager.delete_custom_track(1)
