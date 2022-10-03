import os
from typing import Callable

import discord


class DiscordClient:
    discord_token: str = None

    def __init__(self):
        self.discord_token = os.getenv('DISCORD_TOKEN')

    def connect(self, on_connect: Callable[[discord.Client], None]):
        client = discord.Client(intents=discord.Intents.default())

        @client.event
        async def on_ready():
            print(f'{client.user} has connected to Discord!')

            await on_connect(client)

        client.run(self.discord_token)
