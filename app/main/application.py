import discord

from tasks.health_check.setup import HealthCheckManager
from tasks.office_attendance.setup import OfficeAttendanceManager

from config.discord_client import DiscordClient


class Application:
    discord_client = None

    def run(self):
        self.discord_client = DiscordClient()

        async def on_connect(client: discord.Client):
            await self.setup_tasks(client)

        self.discord_client.connect(on_connect)

    async def setup_tasks(self, client: discord.Client):
        await OfficeAttendanceManager().setup(client)
        await HealthCheckManager().setup(client)
