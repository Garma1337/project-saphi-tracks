# coding: utf-8

import uuid
from datetime import datetime
from unittest import TestCase

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
from api.database.model.resource import Resource
from api.database.model.user import User
from api.http.request_handlers.findcustomtracks import FindCustomTracks
from api.tests.mockmodelrepository import MockModelRepository


class FindCustomTracksTest(TestCase):

    def setUp(self):
        self.user_repository = MockModelRepository(User)
        self.resource_repository = MockModelRepository(Resource)
        self.custom_track_repository = MockModelRepository(CustomTrack)

        self.garma = self.user_repository.create(
            email=f'{str(uuid.uuid4())}@domain.com',
            username=f'Garma',
            password='abcdefg12345678',
            created=datetime.now(),
            verified=True
        )

        self.custom_tracks = [
            self.custom_track_repository.create(
                author_id=self.garma.id,
                name=f'Custom Track {i}',
                description=f'This is a really cool description for Custom Track {i}',
                highlighted=True if i % 2 == 0 else False,
                verified=True if i % 2 == 0 else False,
                created=datetime.now()
            ) for i in range(1, 6)
        ]

        self.request_handler = FindCustomTracks(
            EntityManager(
                SQLAlchemy(),
                MockModelRepository
            ),
            LogicalPermissionResolver()
        )

        self.request_handler.entity_manager.get_repository = lambda model: self.custom_track_repository

    def test_can_find_custom_tracks(self):
        response = self.request_handler.handle_request(Request.from_values())
        data = response.get_data()

        custom_tracks = data['items']
        pagination = data['pagination']

        self.assertEqual(5, len(custom_tracks))
        self.assertEqual(5, pagination['total_item_count'])
        self.assertEqual(20, pagination['items_per_page'])
        self.assertEqual(1, pagination['current_page'])

        self.assertEqual(1, custom_tracks[0]['id'])
        self.assertEqual(2, custom_tracks[1]['id'])
        self.assertEqual(3, custom_tracks[2]['id'])
        self.assertEqual(4, custom_tracks[3]['id'])
        self.assertEqual(5, custom_tracks[4]['id'])

    def test_can_find_custom_tracks_by_id(self):
        response = self.request_handler.handle_request(Request.from_values(query_string='id=1'))
        data = response.get_data()

        custom_tracks = data['items']
        pagination = data['pagination']

        self.assertEqual(1, len(custom_tracks))
        self.assertEqual(1, pagination['total_item_count'])
        self.assertEqual(20, pagination['items_per_page'])
        self.assertEqual(1, pagination['current_page'])

        self.assertEqual(1, custom_tracks[0]['id'])
        self.assertEqual(1, custom_tracks[0]['author_id'])
        self.assertEqual('Custom Track 1', custom_tracks[0]['name'])
        self.assertEqual(False, custom_tracks[0]['highlighted'])
        self.assertEqual(False, custom_tracks[0]['verified'])

    def test_can_find_custom_tracks_by_author_id(self):
        response = self.request_handler.handle_request(Request.from_values(query_string='author_id=2'))
        data = response.get_data()

        custom_tracks = data['items']
        pagination = data['pagination']

        self.assertEqual(0, len(custom_tracks))
        self.assertEqual(0, pagination['total_item_count'])
        self.assertEqual(20, pagination['items_per_page'])
        self.assertEqual(1, pagination['current_page'])

    def test_can_find_custom_tracks_by_name(self):
        response = self.request_handler.handle_request(Request.from_values(query_string='name=Custom Track 2'))
        data = response.get_data()

        custom_tracks = data['items']
        pagination = data['pagination']

        self.assertEqual(1, len(custom_tracks))
        self.assertEqual(1, pagination['total_item_count'])
        self.assertEqual(20, pagination['items_per_page'])
        self.assertEqual(1, pagination['current_page'])

        self.assertEqual(2, custom_tracks[0]['id'])
        self.assertEqual(1, custom_tracks[0]['author_id'])
        self.assertEqual('Custom Track 2', custom_tracks[0]['name'])
        self.assertEqual(True, custom_tracks[0]['highlighted'])
        self.assertEqual(True, custom_tracks[0]['verified'])

    def test_can_find_custom_tracks_by_highlighted(self):
        response = self.request_handler.handle_request(Request.from_values(query_string='highlighted=1'))
        data = response.get_data()

        custom_tracks = data['items']
        pagination = data['pagination']

        self.assertEqual(2, len(custom_tracks))
        self.assertEqual(2, pagination['total_item_count'])
        self.assertEqual(20, pagination['items_per_page'])
        self.assertEqual(1, pagination['current_page'])

        self.assertEqual(2, custom_tracks[0]['id'])
        self.assertEqual(4, custom_tracks[1]['id'])

    def test_can_find_custom_tracks_by_verified(self):
        response = self.request_handler.handle_request(Request.from_values(query_string='verified=1'))
        data = response.get_data()

        custom_tracks = data['items']
        pagination = data['pagination']

        self.assertEqual(2, len(custom_tracks))
        self.assertEqual(2, pagination['total_item_count'])
        self.assertEqual(20, pagination['items_per_page'])
        self.assertEqual(1, pagination['current_page'])

        self.assertEqual(2, custom_tracks[0]['id'])
        self.assertEqual(4, custom_tracks[1]['id'])
