import discord

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
        office_attendance_manager = OfficeAttendanceManager()

        await office_attendance_manager.setup(client)
