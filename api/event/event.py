# coding: utf-8

class Event(object):

    def __init__(self, name: str, context: dict):
        self.name = name
        self.context = context
