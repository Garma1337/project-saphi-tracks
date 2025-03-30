# coding: utf-8

from typing import Optional

from api.discord.discordclient import DiscordClient
from api.discord.discordguildwidget import DiscordGuildWidget, DiscordGuildWidgetMember


class Discord(object):

    def __init__(self, discord_client: DiscordClient):
        self.discord_client = discord_client

    def get_guild_widget(self, guild_id: str) -> Optional[DiscordGuildWidget]:
        content = self.discord_client.get_guild_widget(guild_id)

        if content is None:
            return None

        members = []
        for member in content.get('members', []):
            members.append(DiscordGuildWidgetMember(
                member.get('id'),
                member.get('username'),
                member.get('status'),
                member.get('avatar_url')
            ))

        return DiscordGuildWidget(
            content.get('id'),
            content.get('name'),
            content.get('instant_invite'),
            content.get('presence_count'),
            members
        )
