# coding: utf-8

import uuid
from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.auth.permission.logicalpermissionresolver import LogicalPermissionResolver
from api.auth.sessionmanager import SessionManager
from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
from api.database.model.permission import Permission
from api.database.model.resource import Resource
from api.database.model.user import User
from api.http.request_handlers.findcustomtracks import FindCustomTracks
from api.tests.mockmodelrepository import MockModelRepository


class FindCustomTracksTest(TestCase):

    def setUp(self):
        self.db = SQLAlchemy()
        self.entity_manager = EntityManager(self.db, MockModelRepository)

        self.session_manager = SessionManager(self.entity_manager)
        self.permission_resolver = LogicalPermissionResolver()

        self.user_repository = MockModelRepository(self.db, User)
        self.resource_repository = MockModelRepository(self.db, Resource)
        self.custom_track_repository = MockModelRepository(self.db, CustomTrack)

        self.garma = self.user_repository.create(
            email=f'{str(uuid.uuid4())}@domain.com',
            username=f'Garma',
            password='abcdefg12345678',
            created=datetime.now(),
            verified=True
        )

        self.garma.permission = Permission(
            can_edit_custom_tracks=True,
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

        self.entity_manager.cache_repository_instance(CustomTrack, self.custom_track_repository)
        self.entity_manager.cache_repository_instance(Resource, self.resource_repository)
        self.entity_manager.cache_repository_instance(User, self.user_repository)

        self.request_handler = FindCustomTracks(
            self.entity_manager,
            self.session_manager,
            self.permission_resolver
        )

        self.request_handler.get_current_identity = Mock(return_value=self.garma.to_dictionary())

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

    def test_can_find_highlighted_custom_tracks(self):
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

    def test_can_find_unhighlighted_custom_tracks(self):
        response = self.request_handler.handle_request(Request.from_values(query_string='highlighted=0'))
        data = response.get_data()

        custom_tracks = data['items']
        pagination = data['pagination']

        self.assertEqual(3, len(custom_tracks))
        self.assertEqual(3, pagination['total_item_count'])
        self.assertEqual(20, pagination['items_per_page'])
        self.assertEqual(1, pagination['current_page'])

        self.assertEqual(1, custom_tracks[0]['id'])
        self.assertEqual(3, custom_tracks[1]['id'])
        self.assertEqual(5, custom_tracks[2]['id'])

    def test_can_find_verified_custom_tracks_if_user_has_permission(self):
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

    def test_cannot_find_unverified_custom_tracks_if_user_has_no_permission(self):
        self.garma.permission.can_edit_custom_tracks = False

        response = self.request_handler.handle_request(Request.from_values(query_string='verified=0'))
        data = response.get_data()

        custom_tracks = data['items']
        pagination = data['pagination']

        self.assertEqual(2, len(custom_tracks))
        self.assertEqual(2, pagination['total_item_count'])
        self.assertEqual(20, pagination['items_per_page'])
        self.assertEqual(1, pagination['current_page'])

        self.assertEqual(2, custom_tracks[0]['id'])
        self.assertEqual(4, custom_tracks[1]['id'])

    def test_can_find_unverified_custom_tracks_if_user_has_permission(self):
        response = self.request_handler.handle_request(Request.from_values(query_string='verified=0'))
        data = response.get_data()

        custom_tracks = data['items']
        pagination = data['pagination']

        self.assertEqual(3, len(custom_tracks))
        self.assertEqual(3, pagination['total_item_count'])
        self.assertEqual(20, pagination['items_per_page'])
        self.assertEqual(1, pagination['current_page'])

        self.assertEqual(1, custom_tracks[0]['id'])
        self.assertEqual(3, custom_tracks[1]['id'])
        self.assertEqual(5, custom_tracks[2]['id'])
