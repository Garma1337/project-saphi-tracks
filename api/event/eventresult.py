# coding: utf-8

class EventResult(object):

    def __init__(self, event_name: str, event_subscriber_name: str, context: dict):
        self.event_name = event_name
        self.event_subscriber_name = event_subscriber_name
        self.context = context
