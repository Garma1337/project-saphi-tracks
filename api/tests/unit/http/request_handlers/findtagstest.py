# coding: utf-8

from unittest import TestCase

from flask import Request
from flask_sqlalchemy import SQLAlchemy

from api.database.entitymanager import EntityManager
from api.database.model.tag import Tag
from api.http.request_handlers.findtags import FindTags
from api.tests.mockmodelrepository import MockModelRepository


class FindTagsTest(TestCase):

    def setUp(self):
        self.find_tags = FindTags(
            EntityManager(
                SQLAlchemy(),
                MockModelRepository
            )
        )

        self.tag_repository = MockModelRepository(Tag)

        self.remake = self.tag_repository.create(name='Remake')
        self.difficult = self.tag_repository.create(name='Difficult')

        self.find_tags.entity_manager.get_repository = lambda model: self.tag_repository

    def test_can_find_tags(self):
        response = self.find_tags.handle_request(Request.from_values())

        data = response.get_data()

        tags = data['items']
        pagination = data['pagination']

        self.assertEqual(len(tags), 2)
        self.assertEqual(pagination['current_page'], 1)
        self.assertEqual(pagination['items_per_page'], 20)
        self.assertEqual(pagination['total_item_count'], 2)

        self.assertEqual(tags[0]['id'], self.remake.id)
        self.assertEqual(tags[0]['name'], 'Remake')

        self.assertEqual(tags[1]['id'], self.difficult.id)
        self.assertEqual(tags[1]['name'], 'Difficult')

    def test_can_find_tags_by_id(self):
        response = self.find_tags.handle_request(Request.from_values(query_string='id=1'))

        data = response.get_data()

        tags = data['items']
        pagination = data['pagination']

        self.assertEqual(len(tags), 1)
        self.assertEqual(pagination['current_page'], 1)
        self.assertEqual(pagination['items_per_page'], 20)
        self.assertEqual(pagination['total_item_count'], 1)

        self.assertEqual(tags[0]['id'], self.remake.id)
        self.assertEqual(tags[0]['name'], 'Remake')

    def test_can_find_tags_by_name(self):
        response = self.find_tags.handle_request(Request.from_values(query_string='name=Difficult'))

        data = response.get_data()

        tags = data['items']
        pagination = data['pagination']

        self.assertEqual(len(tags), 1)
        self.assertEqual(pagination['current_page'], 1)
        self.assertEqual(pagination['items_per_page'], 20)
        self.assertEqual(pagination['total_item_count'], 1)

        self.assertEqual(tags[0]['id'], self.difficult.id)
        self.assertEqual(tags[0]['name'], 'Difficult')
