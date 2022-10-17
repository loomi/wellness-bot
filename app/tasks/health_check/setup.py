import discord

from tasks.health_check.services.health_check_service import HealthCheckService
from protocols.task_manager import ITaskManager


class HealthCheckManager(ITaskManager):
    async def setup(self, client: discord.Client):
        health_check_service = HealthCheckService(client)

        await health_check_service.execute()
