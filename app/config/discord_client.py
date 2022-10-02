import os
import discord


class DiscordClient:
    client = None

    def __init__(self):
        DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

        client = discord.Client(intents=discord.Intents.default())

        @client.event
        async def on_ready():
            print(f'{client.user} has connected to Discord!')

        client.run(DISCORD_TOKEN)

        self.client = client
