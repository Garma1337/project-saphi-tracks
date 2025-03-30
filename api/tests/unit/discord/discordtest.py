# coding: utf-8

from unittest import TestCase
from unittest.mock import Mock

from api.discord.discord import Discord
from api.discord.discordclient import DiscordClient
from api.tests.fixtures import mock_discord_guild_widget


class DiscordTest(TestCase):

    def setUp(self):
        self.discord_client = DiscordClient()
        self.discord = Discord(self.discord_client)

        self.discord_client.get_guild_widget = Mock(return_value=mock_discord_guild_widget())

    def test_can_get_guild_widget(self):
        guild_id = '1258355416807772171'
        widget = self.discord.get_guild_widget(guild_id)

        self.assertIsNotNone(widget)

        self.assertEqual(widget.id, '123456789012345678')
        self.assertEqual(widget.name, 'Test Discord')
        self.assertEqual(widget.invite_link, 'https://discord.com/invite/AbCdEfG12')
        self.assertEqual(widget.member_count, 3)

        self.assertEqual(len(widget.members), 3)
        self.assertEqual(widget.members[0].username, 'Garma')
        self.assertEqual(widget.members[1].username, 'Niikasd')
        self.assertEqual(widget.members[2].username, 'Redhot')

    def test_can_not_get_guild_widget_if_request_fails(self):
        self.discord_client.get_guild_widget = Mock(return_value=None)

        guild_id = '1258355416807772171'
        widget = self.discord.get_guild_widget(guild_id)

        self.assertIsNone(widget)
