# coding: utf-8

from unittest import TestCase

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.auth.sessionmanager import SessionManager
from api.database.entitymanager import EntityManager
from api.http.request_handlers.createcustomtrack import CreateCustomTrack
from api.lib.customtrackmanager import CustomTrackManager
from api.lib.semvervalidator import SemVerValidator
from api.resource.file_encoder_strategy.sha256fileencoderstrategy import Sha256FileEncoderStrategy
from api.resource.resourcemanager import ResourceManager
from api.tests.mockfilesystemadapter import MockFileSystemAdapter
from api.tests.mockmodelrepository import MockModelRepository


class CreateCustomTrackTest(TestCase):

    def setUp(self):
        self.entity_manager = EntityManager(SQLAlchemy(), MockModelRepository)

        self.session_manager = SessionManager(self.entity_manager)

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

        self.create_custom_track = CreateCustomTrack(self.session_manager, self.custom_track_manager)

    def test_can_create_custom_track(self):
        pass

    def test_can_not_create_custom_track_when_name_is_missing(self):
        request = Request.from_values(data={
            'description': 'Test description',
            'video': 'https://www.youtube.com/watch?v=SB3wAJjJP6c',
            'lev_file_version': '1.2.3',
            'vrm_file_version': '1.2.3',
        })

        response = self.create_custom_track.handle_request(request)
        data = response.get_data()

        self.assertEqual(response.get_status_code(), 400)
        self.assertIsNotNone(data['error'])

    def test_can_not_create_custom_track_when_description_is_missing(self):
        request = Request.from_values(data={
            'name': 'Test',
            'video': 'https://www.youtube.com/watch?v=SB3wAJjJP6c',
            'lev_file_version': '1.2.3',
            'vrm_file_version': '1.2.3',
        })

        response = self.create_custom_track.handle_request(request)
        data = response.get_data()

        self.assertEqual(response.get_status_code(), 400)
        self.assertIsNotNone(data['error'])

    def test_can_not_create_custom_track_when_video_is_missing(self):
        request = Request.from_values(data={
            'name': 'Test',
            'description': 'Test description',
            'lev_file_version': '1.2.3',
            'vrm_file_version': '1.2.3',
        })

        response = self.create_custom_track.handle_request(request)
        data = response.get_data()

        self.assertEqual(response.get_status_code(), 400)
        self.assertIsNotNone(data['error'])

    def test_can_not_create_custom_track_when_lev_file_version_is_missing(self):
        request = Request.from_values(data={
            'name': 'Test',
            'description': 'Test description',
            'video': 'https://www.youtube.com/watch?v=SB3wAJjJP6c',
            'vrm_file_version': '1.2.3',
        })

        response = self.create_custom_track.handle_request(request)
        data = response.get_data()

        self.assertEqual(response.get_status_code(), 400)
        self.assertIsNotNone(data['error'])

    def test_can_not_create_custom_track_when_vrm_file_version_is_missing(self):
        request = Request.from_values(data={
            'name': 'Test',
            'description': 'Test description',
            'video': 'https://www.youtube.com/watch?v=SB3wAJjJP6c',
            'lev_file_version': '1.2.3',
        })

        response = self.create_custom_track.handle_request(request)
        data = response.get_data()

        self.assertEqual(response.get_status_code(), 400)
        self.assertIsNotNone(data['error'])
