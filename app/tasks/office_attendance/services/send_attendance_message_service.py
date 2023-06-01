import datetime

import discord
from discord.ext import tasks
from protocols.task_service import ITaskService


class SendAttendanceMessageService(ITaskService):
    client: discord.Client = None

    async def send_message(self):
        weekday = datetime.datetime.now().weekday()

        weekdays = ['Segunda-feira', 'Terça-feira', 'Quarta-feira',
            'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']

        weekday_string = weekdays[weekday]

        message = datetime.date.today().strftime(f'{weekday_string}, %d/%m:')

        channels = self.client.get_all_channels()

        target_channel = discord.utils.get(channels, name='dia-de-office')

        if not target_channel:
            return

        message = await self.client.get_channel(target_channel.id).send(message)

        emojis = ['📍', '💻', '🕰️']

        for emoji in emojis:
            await message.add_reaction(emoji)

    async def execute(self):
        # UTC-03:00
        timezone = datetime.timezone(datetime.timedelta(hours=-3))

        message_time = datetime.time(hour=7, minute=0, tzinfo=timezone)

        @tasks.loop(time=[message_time])
        async def send_message_task():
            # Won't execute on the weekend
            if datetime.datetime.today().weekday() < 5:
                await self.send_message()

        send_message_task.start()
