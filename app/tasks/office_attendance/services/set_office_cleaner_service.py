import re
import random
import discord
import datetime
from discord.ext import tasks

from protocols.task_service import ITaskService

DEFAULT_UELNISON_ID = 1112809679672852624
DEMAND_HOUR = 15
DEMAND_MINUTE = 0
DEMAND_SECOND = 0

class SetOfficeCleanerService(ITaskService):
    client: discord.Client = None

    async def get_messages(self):
        today = datetime.datetime.now()

        start_date = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)  # today at 00:00
        end_date = start_date + datetime.timedelta(days=1)  # tomorrow at 00:00
        yesterday_start_date = start_date - datetime.timedelta(days=1)  # yesterday at 00:00
        yesterday_end_date = start_date - datetime.timedelta(days=0)  # today at 00:00

        today_start_datetime = datetime.datetime.strptime(start_date.strftime('%d/%m/%Y'), '%d/%m/%Y')
        today_end_datetime = datetime.datetime.strptime(end_date.strftime('%d/%m/%Y'), '%d/%m/%Y')
        yesterday_start_datetime = datetime.datetime.strptime(yesterday_start_date.strftime('%d/%m/%Y'), '%d/%m/%Y')
        yesterday_end_datetime = datetime.datetime.strptime(yesterday_end_date.strftime('%d/%m/%Y'), '%d/%m/%Y')

        channels = self.client.get_all_channels()
        target_channel = discord.utils.get(channels, name='liderança')

        today_message_history = target_channel.history(after=today_start_datetime, before=today_end_datetime)
        today_all_messages = [message async for message in today_message_history]
        yesterday_message_history = target_channel.history(after=yesterday_start_datetime, before=yesterday_end_datetime)
        yesterday_all_messages = [message async for message in yesterday_message_history]

        weekdays = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
        weekdays_or_expression = '|'.join(weekdays)
        day_format_expression = '([0-9]{2})/([0-9]{2})'

        pattern = re.compile(f'^({weekdays_or_expression}), {day_format_expression}:$')
        user_picked_pattern = re.compile(f'^(Parabéns)')

        attendance_messages = list(filter(lambda message: pattern.match(message.content), today_all_messages))
        picked_yesterday = list(filter(lambda message: user_picked_pattern.match(message.content), yesterday_all_messages))

        return [attendance_messages, picked_yesterday]

    async def demand_cleaner(self):
        [messages_to_handle, picked_messages] = await self.get_messages()

        reactions = [reaction for message in messages_to_handle for reaction in message.reactions]

        users_to_be_raffled = []

        for reaction in reactions:
            async for user in reaction.users():
                if reaction.emoji == '📍':
                    users_to_be_raffled.append(user.id)
                if reaction.emoji == '🕰️':
                    users_to_be_raffled.append(user.id)
                    users_to_be_raffled.append(user.id)

        user_picked_message = None
        if len(picked_messages) > 0:
            user_picked_message = picked_messages[0]

        user_raffled_yesterday_id = DEFAULT_UELNISON_ID
        if user_picked_message is not None:
            user_raffled_yesterday_id = user_picked_message.mentions[0].id

        users_to_be_raffled_without_user_picked = list(
            filter(
                lambda user_id: (
                    user_id != user_raffled_yesterday_id and user_id != DEFAULT_UELNISON_ID
                ), users_to_be_raffled
            )
        )

        channels = self.client.get_all_channels()
        target_channel = discord.utils.get(channels, name='liderança')

        if len(users_to_be_raffled_without_user_picked) == 0:
            is_not_uelnison_user_raffled = user_raffled_yesterday_id != DEFAULT_UELNISON_ID
            is_only_user_raffled = user_raffled_yesterday_id in users_to_be_raffled

            if is_not_uelnison_user_raffled and is_only_user_raffled:
                message = f'Parabéns <@{user_raffled_yesterday_id}>!\nAliás, já vai me desculpando, mas eu só tinha você. Então você é, outra vez, responsável pela limpeza do office hoje! 🥳 🧹'
                await self.client.get_channel(target_channel.id).send(message)
            else:
                message = f'É impressão minha ou niguém apareceu no office hoje!? 🤨'
                await self.client.get_channel(target_channel.id).send(message)
        else:
            user_picked_today_id = random.choice(
                users_to_be_raffled_without_user_picked)

            message = f'Parabéns <@{user_picked_today_id}>!\nVocê é responsável pela limpeza do office hoje! 🥳 🧹'
            await self.client.get_channel(target_channel.id).send(message)

    async def execute(self):
        # UTC-03:00
        timezone = datetime.timezone(datetime.timedelta(hours=-3))

        message_time = datetime.time(hour=DEMAND_HOUR, minute=DEMAND_MINUTE, second=DEMAND_SECOND, tzinfo=timezone)

        @tasks.loop(time=[message_time])
        async def demand_cleaner_task():
            # Won't execute on the weekend
            if datetime.datetime.today().weekday() < 5:
                await self.demand_cleaner()

        demand_cleaner_task.start()
