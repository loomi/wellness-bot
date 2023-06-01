import os
import discord
from typing import Callable
from discord.ext import commands

from event_managers.on_message import on_message_event_handler
from tasks.office_attendance.services.block_delayed_reactions_service import block_delayed_reaction_service

class DiscordClient:
    discord_token: str = None

    def __init__(self):
        self.discord_token = os.getenv('DISCORD_TOKEN')

    def connect(self, on_connect: Callable[[discord.Client], None]):
        client = commands.Bot(command_prefix='/', intents=discord.Intents.all())
        # client = discord.Client(intents=discord.Intents.default())

        @client.event
        async def on_ready():
            print(f'{client.user} has connected to Discord!')

            await on_connect(client)

            try:
                await client.tree.sync()
            except Exception as e:
                print(e)

        @client.tree.command(name='enviar_mensagem')
        @discord.app_commands.describe(sua_mensagem = 'Mensagem a ser enviada')
        @discord.app_commands.describe(canal = 'Canal para mensagem ser enviada')
        @discord.app_commands.choices(canal = [
            discord.app_commands.Choice(name='step_by_step', value='step_by_step'),
            discord.app_commands.Choice(name='lideranca', value='lideranca'),
            discord.app_commands.Choice(name='scripts', value='scripts')
        ])
        async def enviar_mensagem(
            interaction: discord.Interaction,
            sua_mensagem: str,
            canal: str
        ):
            await interaction.response.defer()
            available_channels = {
                "step_by_step": 928632701941059655,
                "lideranca": 971875026628378624,
                "scripts": 918547745046937630,
            }
            if (canal not in available_channels):
                await interaction.followup.send(content="Canal não encontrado")
                return

            await interaction.followup.send(content='Mandei sua mensagem lá no canal!')

            channel = client.get_channel(available_channels[canal])
            await channel.send(content=sua_mensagem)


        @client.event
        async def on_raw_reaction_add(reaction: discord.RawReactionActionEvent):
            await block_delayed_reaction_service(client, reaction)

        @client.event
        async def on_message(message):
            await on_message_event_handler.call_handlers(message)

        client.run(self.discord_token)
