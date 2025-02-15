# coding: utf-8

from unittest import TestCase

from api.event.event import Event
from api.event.eventsubscriber import EventSubscriber
from api.event.eventmanager import EventManager


class CustomTrackCreatedEventSubscriber(EventSubscriber):

    def run_on_event(self, event):
        return { 'track': 'verified' }

    def get_event_name(self):
        return 'custom_track_created'

    def get_name(self):
        return 'custom_track_created_event_subscriber'


class UserLoginEventSubscriber(EventSubscriber):

    def run_on_event(self, event):
        return { 'access': 'denied' }

    def get_event_name(self):
        return 'user_logged_in'

    def get_name(self):
        return 'user_login_event_subscriber'


class EventManagerTest(TestCase):

    def setUp(self):
        self.event_manager = EventManager()

    def test_can_register_event_subscriber(self):
        event_subscriber = UserLoginEventSubscriber()
        self.event_manager.register_event_subscriber(event_subscriber)

        subscribers = self.event_manager.get_event_subscribers_for_event('user_logged_in')

        self.assertEqual(1, len(subscribers))
        self.assertEqual(event_subscriber, subscribers[0])

    def test_can_register_multiple_event_subscribers(self):
        user_login_event_subscriber = UserLoginEventSubscriber()
        custom_track_created_event_subscriber = CustomTrackCreatedEventSubscriber()

        self.event_manager.register_event_subscriber(user_login_event_subscriber)
        self.event_manager.register_event_subscriber(custom_track_created_event_subscriber)

        user_login_subscribers = self.event_manager.get_event_subscribers_for_event('user_logged_in')
        custom_track_created_subscribers = self.event_manager.get_event_subscribers_for_event('custom_track_created')

        self.assertEqual(1, len(user_login_subscribers))
        self.assertEqual(user_login_event_subscriber, user_login_subscribers[0])

        self.assertEqual(1, len(custom_track_created_subscribers))
        self.assertEqual(custom_track_created_event_subscriber, custom_track_created_subscribers[0])

    def test_can_not_register_event_subscriber_twice(self):
        event_subscriber = UserLoginEventSubscriber()
        self.event_manager.register_event_subscriber(event_subscriber)

        with self.assertRaises(ValueError):
            self.event_manager.register_event_subscriber(event_subscriber)

    def test_can_not_register_event_subscriber_with_invalid_type(self):
        with self.assertRaises(ValueError):
            self.event_manager.register_event_subscriber('invalid_subscriber')

    def test_can_get_event_subscribers_for_event(self):
        user_login_event_subscriber = UserLoginEventSubscriber()
        custom_track_created_event_subscriber = CustomTrackCreatedEventSubscriber()

        self.event_manager.register_event_subscriber(user_login_event_subscriber)
        self.event_manager.register_event_subscriber(custom_track_created_event_subscriber)

        user_login_subscribers = self.event_manager.get_event_subscribers_for_event('user_logged_in')
        custom_track_created_subscribers = self.event_manager.get_event_subscribers_for_event('custom_track_created')

        self.assertEqual(1, len(user_login_subscribers))
        self.assertEqual(user_login_event_subscriber, user_login_subscribers[0])

        self.assertEqual(1, len(custom_track_created_subscribers))
        self.assertEqual(custom_track_created_event_subscriber, custom_track_created_subscribers[0])

    def test_can_get_empty_list_when_no_subscribers_registered_for_event(self):
        subscribers = self.event_manager.get_event_subscribers_for_event('user_logged_in')
        self.assertEqual([], subscribers)

    def test_can_get_registered_event_subscribers(self):
        user_login_event_subscriber = UserLoginEventSubscriber()
        custom_track_created_event_subscriber = CustomTrackCreatedEventSubscriber()

        self.event_manager.register_event_subscriber(user_login_event_subscriber)
        self.event_manager.register_event_subscriber(custom_track_created_event_subscriber)

        subscribers = self.event_manager.get_registered_event_subscribers()

        self.assertEqual(2, len(subscribers))
        self.assertEqual(1, len(subscribers['user_logged_in']))
        self.assertEqual(1, len(subscribers['custom_track_created']))

        self.assertEqual(user_login_event_subscriber, subscribers['user_logged_in'][0])
        self.assertEqual(custom_track_created_event_subscriber, subscribers['custom_track_created'][0])

    def test_can_get_empty_list_when_no_subscribers_registered(self):
        subscribers = self.event_manager.get_registered_event_subscribers()

        self.assertEqual({}, subscribers)

    def test_can_check_if_event_subscriber_is_registered(self):
        user_login_event_subscriber = UserLoginEventSubscriber()
        custom_track_created_event_subscriber = CustomTrackCreatedEventSubscriber()

        self.event_manager.register_event_subscriber(user_login_event_subscriber)
        self.event_manager.register_event_subscriber(custom_track_created_event_subscriber)

        self.assertTrue(self.event_manager.is_event_subscriber_registered(user_login_event_subscriber))
        self.assertTrue(self.event_manager.is_event_subscriber_registered(custom_track_created_event_subscriber))

    def test_can_check_if_event_subscriber_is_not_registered(self):
        user_login_event_subscriber = UserLoginEventSubscriber()
        custom_track_created_event_subscriber = CustomTrackCreatedEventSubscriber()

        self.assertFalse(self.event_manager.is_event_subscriber_registered(user_login_event_subscriber))
        self.assertFalse(self.event_manager.is_event_subscriber_registered(custom_track_created_event_subscriber))

    def test_can_fire_event(self):
        user_login_event_subscriber = UserLoginEventSubscriber()
        custom_track_created_event_subscriber = CustomTrackCreatedEventSubscriber()

        self.event_manager.register_event_subscriber(user_login_event_subscriber)
        self.event_manager.register_event_subscriber(custom_track_created_event_subscriber)

        results1 = self.event_manager.fire_event(Event('user_logged_in', { 'user_id': 1 }))
        results2 = self.event_manager.fire_event(Event('custom_track_created', { 'track_id': 1 }))

        self.assertEqual(1, len(results1))
        self.assertEqual('user_logged_in', results1[0].event_name)
        self.assertEqual('user_login_event_subscriber', results1[0].event_subscriber_name)
        self.assertEqual({ 'access': 'denied' }, results1[0].context)

        self.assertEqual(1, len(results2))
        self.assertEqual('custom_track_created', results2[0].event_name)
        self.assertEqual('custom_track_created_event_subscriber', results2[0].event_subscriber_name)
        self.assertEqual({ 'track': 'verified' }, results2[0].context)
