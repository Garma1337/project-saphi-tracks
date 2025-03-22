# coding: utf-8

from unittest import TestCase

from flask_sqlalchemy import SQLAlchemy

from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
from api.database.model.resource import Resource
from api.lib.customtrackmanager import CustomTrackManager, CustomTrackNotFoundError, CustomTrackAlreadyVerifiedError
from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy
from api.resource.resourcemanager import ResourceManager
from api.tests.mockfilesystemadapter import MockFileSystemAdapter
from api.tests.mockmodelrepository import MockModelRepository


class CustomTrackManagerTest(TestCase):

    def setUp(self):
        self.custom_track_repository = MockModelRepository(CustomTrack)
        self.resource_repository = MockModelRepository(Resource)

        self.file_system_adapter = MockFileSystemAdapter()
        self.file_encoder_strategy = Sha256FileEncoderStrategy()

        self.resource_manager = ResourceManager(
            EntityManager(SQLAlchemy(), MockModelRepository),
            self.file_system_adapter,
            self.file_encoder_strategy
        )

        self.custom_track_manager = CustomTrackManager(
            EntityManager(SQLAlchemy(), MockModelRepository),
            self.resource_manager
        )

        self.resource_manager.entity_manager.get_repository = lambda model: self.resource_repository
        self.custom_track_manager.entity_manager.get_repository = lambda model: self.custom_track_repository

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
