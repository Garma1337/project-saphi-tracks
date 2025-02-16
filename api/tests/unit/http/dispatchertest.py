# coding: utf-8

from unittest import TestCase

from api.http.dispatcher import Dispatcher
from api.http.router import Router


class DispatcherTest(TestCase):

    def setUp(self):
        self.router = Router()
        self.dispatcher = Dispatcher(self.router)
