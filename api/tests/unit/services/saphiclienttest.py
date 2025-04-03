# coding: utf-8

from json import JSONDecodeError
from unittest import TestCase
from unittest.mock import Mock

import requests
from requests import RequestException, Response

from api.services.saphiclient import SaphiClient


class SaphiClientTest(TestCase):

    def setUp(self):
        self.saphi_client = SaphiClient('http://127.0.0.1/api', 'test')

    def test_can_validate_user_credentials(self):
        self.saphi_client._try_post_request = Mock(return_value={
            'success': True,
            'user_data': {
                'id': 1,
                'username': 'Garma'
            }
        })

        response = self.saphi_client.validate_user_credentials('test', 'test')

        self.assertTrue(response['success'])

    def test_can_not_validate_user_credentials_if_credentials_are_invalid(self):
        self.saphi_client._try_post_request = Mock(return_value={
            'success': False
        })

        response = self.saphi_client.validate_user_credentials('test', 'test')

        self.assertFalse(response['success'])

    def test_can_make_post_request(self):
        response = Response()
        response.json = Mock(return_value={'success': True})

        requests.post = Mock(return_value=response)

        response = self.saphi_client._try_post_request('/test', {})
        self.assertEqual(response, {'success': True})

    def test_can_not_make_post_request_if_request_fails(self):
        requests.post = Mock(side_effect=RequestException('Request failed'))

        response = self.saphi_client._try_post_request('/test', {})
        self.assertEqual(response, {'success': False})

    def test_can_return_empty_response_if_response_is_no_valid_json(self):
        response = Response()
        response.json = Mock(side_effect=JSONDecodeError('Failed to decode JSON', '', 0))
        requests.post = Mock(return_value=response)

        response = self.saphi_client._try_post_request('/test', {})
        self.assertEqual(response, {'success': False})
