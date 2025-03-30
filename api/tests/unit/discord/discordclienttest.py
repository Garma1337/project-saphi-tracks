# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

import requests

from api.discord.discordclient import DiscordClient


class DiscordClientTest(TestCase):

    def setUp(self):
        self.discord_client = DiscordClient()

    def test_can_not_get_guild_widget_if_request_fails(self):
        requests.get = Mock(side_effect=requests.RequestException('Request failed'))

        response = self.discord_client.get_guild_widget('1258355416807772171')
        self.assertIsNone(response)

    def test_can_not_get_guild_widget_if_response_is_no_valid_json(self):
        response = Mock()
        response.json = Mock(side_effect=requests.JSONDecodeError('Failed to decode JSON', '', 0))
        requests.get = Mock(return_value=response)

        response = self.discord_client.get_guild_widget('1258355416807772171')
        self.assertIsNone(response)
