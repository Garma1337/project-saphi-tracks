# coding: utf-8

from unittest import TestCase

from flask_sqlalchemy import SQLAlchemy

from api.database.entitymanager import EntityManager
from api.database.model.setting import Setting
from api.http.request_handlers.findsettings import FindSettings
from api.tests.mockmodelrepository import MockModelRepository


class FindSettingsTest(TestCase):

    def setUp(self):
        self.db = SQLAlchemy()
        self.entity_manager = EntityManager(self.db, MockModelRepository)

        self.setting_repository = MockModelRepository(self.db, Setting)
        self.setting_repository.create(name='TestSetting1', value='Value1')

        self.request_handler = FindSettings(self.entity_manager)

