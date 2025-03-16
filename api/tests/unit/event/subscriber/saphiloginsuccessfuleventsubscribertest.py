# coding: utf-8

from unittest import TestCase

from flask_sqlalchemy import SQLAlchemy

from api.auth.passwordmanager import PasswordManager
from api.auth.user_adapter.saphiuseradapter import SaphiUserAdapter
from api.database.entitymanager import EntityManager
from api.database.model.user import User
from api.event.event import Event
from api.event.eventmanager import EventManager
from api.event.subscribers.saphiloginsuccessfuleventsubscriber import SaphiLoginSuccessfulEventSubscriber
from api.lib.saphiclient import SaphiClient
from api.tests.mockmodelrepository import MockModelRepository
from api.tests.mockpasswordencoderstrategy import MockPasswordEncoderStrategy


class SaphiLoginSuccessfulEventSubscriberTest(TestCase):

    def setUp(self):
        self.event_manager = EventManager()
        self.entity_manager = EntityManager(SQLAlchemy(), MockModelRepository)
        self.user_repository = MockModelRepository(User)
        self.password_manager = PasswordManager(MockPasswordEncoderStrategy())

        self.saphi_login_successful_event_subscriber = SaphiLoginSuccessfulEventSubscriber(
            self.entity_manager,
            self.password_manager
        )

        self.saphi_client = SaphiClient('http://127.0.0.1/api', '123456')

        self.saphi_user_adapter = SaphiUserAdapter(
            self.event_manager,
            self.entity_manager,
            self.password_manager,
            self.saphi_client
        )

        self.entity_manager.get_repository = lambda model: self.user_repository

    def test_can_create_new_user(self):
        result = self.saphi_login_successful_event_subscriber.run_on_event(Event('saphi_login_successful', {
            'username': 'Garma',
            'password': 'Password123!',
            'user_adapter': self.saphi_user_adapter
        }))

        users = self.user_repository.find_by(username='Garma')

        self.assertEqual(len(users), 1)
        self.assertEqual(result['user_created'], True)
        self.assertEqual(result['user_updated'], False)

    def test_can_update_existing_user(self):
        self.user_repository.create(username='Garma', password='Password123!')

        result = self.saphi_login_successful_event_subscriber.run_on_event(Event('saphi_login_successful', {
            'username': 'Garma',
            'password': 'Password123456!',
            'user_adapter': self.saphi_user_adapter
        }))

        users = self.user_repository.find_by(username='Garma')

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].password, 'Password123456!')
        self.assertEqual(result['user_created'], False)
        self.assertEqual(result['user_updated'], True)
