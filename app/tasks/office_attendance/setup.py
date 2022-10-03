import datetime

from discord.ext import tasks
import discord

from tasks.office_attendance.services.send_attendance_message_service import SendAttendanceMessageService
from protocols.task_manager import ITaskManager


class OfficeAttendanceManager(ITaskManager):
    async def setup(self, client: discord.Client):
        send_attendance_message_service = SendAttendanceMessageService(client)

        # UTC-03:00
        timezone = datetime.timezone(datetime.timedelta(hours=-3))

        message_time = datetime.time(hour=7, minute=0, tzinfo=timezone)

        await send_attendance_message_service.execute()

        @tasks.loop(time=[message_time])
        async def send_message_task():
            # Won't execute on the weekend
            if datetime.datetime.today().weekday() < 5:
                await send_attendance_message_service.execute()

        send_message_task.start()
