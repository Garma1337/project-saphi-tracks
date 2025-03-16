# coding: utf-8

from api.event.eventmanager import EventManager
from api.lib.container import Container


class EventManagerFactory(object):

    @staticmethod
    def factory(container: Container):
        event_manager = EventManager()
        event_manager.register_event_subscriber(container.get('event.subscriber.saphi_login_successful'))

        return event_manager
