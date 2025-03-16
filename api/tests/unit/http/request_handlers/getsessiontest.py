# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask import Request

from api.http.request_handlers.getsession import GetSession


class GetSessionTest(TestCase):

    def setUp(self):
        self.get_session = GetSession()

    def test_can_get_session_if_logged_in(self):
        self.get_session.get_current_user = Mock(return_value={'name': 'Garma'})

        response = self.get_session.handle_request(Request.from_values())
        data = response.get_data()

        self.assertEqual(data['current_user'], {'name': 'Garma'})

    def test_can_get_session_if_not_logged_in(self):
        self.get_session.get_current_user = Mock(return_value=None)

        response = self.get_session.handle_request(Request.from_values())
        data = response.get_data()

        self.assertEqual(data['current_user'], None)
