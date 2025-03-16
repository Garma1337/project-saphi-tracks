# coding: utf-8

from json import JSONDecodeError

import requests
from requests import RequestException


class SaphiClient(object):

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def validate_user_credentials(self, username: str, password: str) -> dict:
        body = {
            'username': username,
            'password': password
        }

        return self._try_post_request(f'{self.base_url}/validate-user-credentials', body)

    def _try_post_request(self, url: str, body: dict) -> dict:
        try:
            response = requests.post(url, json = body, headers = {'Saphi-Api-Key': self.api_key})

            print(response.content)

            try:
                return response.json()
            except JSONDecodeError:
                return {'success': False}
        except RequestException as e:
            return {'success': False}
