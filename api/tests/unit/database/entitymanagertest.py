# coding: utf-8

from unittest import TestCase

from flask_sqlalchemy import SQLAlchemy

from api.database.entitymanager import EntityManager
from api.database.model.customtrack import CustomTrack
from api.database.repository.modelrepository import ModelRepository


class EntityManagerTest(TestCase):

    def setUp(self):
        self.entity_manager = EntityManager(SQLAlchemy(), ModelRepository)

    def test_can_get_model_repository(self):
        repository = self.entity_manager.get_repository(CustomTrack)
        self.assertIsInstance(repository, ModelRepository)

    def test_can_get_cached_model_repository(self):
        repository = self.entity_manager.get_repository(CustomTrack)
        cached_repository = self.entity_manager.get_repository(CustomTrack)

        self.assertEqual(repository, cached_repository)
