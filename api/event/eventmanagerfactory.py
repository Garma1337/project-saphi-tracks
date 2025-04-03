# coding: utf-8

from api.di.transientcontainer import TransientContainer
from api.event.eventmanager import EventManager


class EventManagerFactory(object):

    @staticmethod
    def factory(container: TransientContainer):
        event_manager = EventManager()
        event_manager.register_event_subscriber(container.get('event.subscriber.saphi_login_successful'))

        return event_manager
