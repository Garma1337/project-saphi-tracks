# coding: utf-8

from typing import List

from api.event.event import Event
from api.event.eventsubscriber import EventSubscriber
from api.event.eventresult import EventResult


class EventManager(object):

    def __init__(self):
        self.subscribers = {}

    def register_event_subscriber(self, subscriber: EventSubscriber) -> None:
        if not isinstance(subscriber, EventSubscriber):
            raise ValueError(f'Subcriber must be an instance of {EventSubscriber.__class__.__name__}')

        if not subscriber.get_event_name() in self.subscribers:
            self.subscribers[subscriber.get_event_name()] = []

        if self.is_event_subscriber_registered(subscriber):
            raise ValueError(f'Subcriber {subscriber.get_name()} is already registered for event {subscriber.get_event_name()}')

        self.subscribers[subscriber.get_event_name()].append(subscriber)

    def get_event_subscribers_for_event(self, event_name: str) -> List[EventSubscriber]:
        if not event_name in self.subscribers:
            return []

        return self.subscribers[event_name]

    def is_event_subscriber_registered(self, subscriber: EventSubscriber) -> bool:
        if not subscriber.get_event_name() in self.subscribers:
            return False

        return subscriber in self.subscribers[subscriber.get_event_name()]

    def get_registered_event_subscribers(self) -> dict[str, List[EventSubscriber]]:
        return self.subscribers

    def fire_event(self, event: Event) -> List[EventResult]:
        results = []
        event_subscribers = self.get_event_subscribers_for_event(event.name)

        for event_subscriber in event_subscribers:
            result = event_subscriber.run_on_event(event)
            results.append(EventResult(event.name, event_subscriber.get_name(), result))

        return results
