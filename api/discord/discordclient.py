# coding: utf-8

from typing import Optional

import requests
from requests import JSONDecodeError, RequestException


class DiscordClient(object):

    def __init__(self):
        pass

    def get_guild_widget(self, guild_id: str) -> Optional[dict]:
        try:
            response = requests.get(f'https://discord.com/api/guilds/{guild_id}/widget.json')

            try:
                return response.json()
            except JSONDecodeError:
                return None
        except RequestException:
            return None
