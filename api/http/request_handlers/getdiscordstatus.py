# coding: utf-8

from api.discord.discord import Discord
from api.discord.discordguildwidget import DiscordGuildWidgetSchema
from api.http.request_handlers.requesthandler import RequestHandler
from api.http.response import ErrorJsonResponse, SuccessJsonResponse


class GetDiscordStatus(RequestHandler):

    def __init__(self, discord: Discord, guild_id: str):
        self.discord = discord
        self.guild_id = guild_id

    def handle_request(self, request):
        guild_widget = self.discord.get_guild_widget(self.guild_id)

        if guild_widget is None:
            return ErrorJsonResponse('Failed to fetch Discord widget')

        discord_widget_schema = DiscordGuildWidgetSchema()
        return SuccessJsonResponse({'widget': discord_widget_schema.dump(guild_widget)})

    def require_authentication(self) -> bool:
        return False
