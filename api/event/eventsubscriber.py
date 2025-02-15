# coding: utf-8

from abc import abstractmethod, ABC

from api.event.event import Event


class EventSubscriber(ABC):

    @abstractmethod
    def run_on_event(self, event: Event) -> dict:
        pass

    @abstractmethod
    def get_event_name(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
