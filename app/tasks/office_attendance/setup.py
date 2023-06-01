import discord

from protocols.task_manager import ITaskManager

from tasks.office_attendance.services.send_attendance_message_service import SendAttendanceMessageService
from tasks.office_attendance.services.count_attendance_messages_service import CountAttendanceMessagesService
from tasks.office_attendance.services.set_office_cleaner_service import SetOfficeCleanerService


class OfficeAttendanceManager(ITaskManager):
    async def setup(self, client: discord.Client):
        send_attendance_message_service = SendAttendanceMessageService(client)
        count_attendance_messages_service = CountAttendanceMessagesService(client)
        set_office_cleaner_service = SetOfficeCleanerService(client)

        await send_attendance_message_service.execute()
        await count_attendance_messages_service.execute()
        await set_office_cleaner_service.execute()
