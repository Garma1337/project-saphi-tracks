# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from flask import Request

from api.discord.discord import Discord
from api.discord.discordclient import DiscordClient
from api.http.request_handlers.getdiscordstatus import GetDiscordStatus
from api.tests.fixtures import mock_discord_guild_widget


class GetDiscordStatusTest(TestCase):

    def setUp(self):
        self.discord_client = DiscordClient()
        self.discord_client.get_guild_widget = Mock(return_value=mock_discord_guild_widget())

        self.discord = Discord(self.discord_client)
        self.get_discord_status = GetDiscordStatus(self.discord, '123456789012345678')

    def test_can_get_discord_status(self):
        response = self.get_discord_status.handle_request(Request.from_values())
        data = response.get_data()

        self.assertEqual(data['success'], True)
        self.assertEqual(data['widget']['id'], '123456789012345678')
        self.assertEqual(data['widget']['name'], 'Test Discord')
        self.assertEqual(data['widget']['invite_link'], 'https://discord.com/invite/AbCdEfG12')
        self.assertEqual(data['widget']['member_count'], 3)

        self.assertEqual(len(data['widget']['members']), 3)
        self.assertEqual(data['widget']['members'][0]['username'], 'Garma')
        self.assertEqual(data['widget']['members'][1]['username'], 'Niikasd')
        self.assertEqual(data['widget']['members'][2]['username'], 'Redhot')

    def test_can_not_get_discord_status_if_request_fails(self):
        self.discord_client.get_guild_widget = Mock(return_value=None)

        response = self.get_discord_status.handle_request(Request.from_values())
        data = response.get_data()

        self.assertEqual(data['success'], False)
        self.assertFalse('widget' in data)
