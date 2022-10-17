import discord
from event_managers.on_message import on_message_subscriber

from protocols.task_service import ITaskService


class HealthCheckService(ITaskService):
    client: discord.Client = None

    async def execute(self):
        @on_message_subscriber('health-check', is_dm=True)
        async def on_message(message: discord.Message):
            await message.channel.send('Health Checked!')
