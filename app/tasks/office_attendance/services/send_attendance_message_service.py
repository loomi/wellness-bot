from datetime import date, datetime

import discord
from protocols.task_service import ITaskService


class SendAttendanceMessageService(ITaskService):
    client: discord.Client = None

    async def execute(self):
        weekday = datetime.now().weekday()

        weekdays = ['Segunda-feira', 'Terça-feira', 'Quarta-feira',
            'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']

        weekday_string = weekdays[weekday]

        message = date.today().strftime(f'{weekday_string}, %d/%m:')

        channels = self.client.get_all_channels()

        target_channel = discord.utils.get(channels, name='dia-de-office')

        if not target_channel:
            return

        message = await self.client.get_channel(target_channel.id).send(message)

        emojis = ['📍', '💻']

        for emoji in emojis:
            await message.add_reaction(emoji)
