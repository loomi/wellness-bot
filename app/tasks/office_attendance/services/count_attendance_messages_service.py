from datetime import datetime
import re
import io
import discord
from event_managers.on_message import on_message_subscriber
from protocols.task_service import ITaskService


class CountAttendanceMessagesService(ITaskService):
    client: discord.Client = None

    async def execute(self):
        @on_message_subscriber('count-attendance', is_dm=True)
        async def on_message(message: discord.Message):
            date_regex = '[0-9]{2}/[0-9]{2}/[0-9]{4}'
            message_regex = f'^!count-attendance ({date_regex})( {date_regex})?$'
            message_pattern = re.compile(message_regex)

            match = message_pattern.match(message.content)

            if not match:
                error_message = 'Formato inválido, exemplo:\n' \
                    '**!count-attendance [data inicial]**'

                await message.channel.send(error_message)

                return

            matched_groups = [
                group.strip() if group else None for group in match.groups()]

            start_date, *rest = matched_groups

            end_date = (rest[0] if rest else None)

            try:
                datetime.strptime(start_date, '%d/%m/%Y')
                if end_date:
                    datetime.strptime(end_date, '%d/%m/%Y')
            except ValueError:
                error_message = 'Formato de data inválido, o formato correto é DD/MM/YYYY'

                await message.channel.send(error_message)

                return

            now = datetime.now()
            now_formatted = datetime.now().strftime('%d/%m/%Y')
            start_datetime = datetime.strptime(start_date, '%d/%m/%Y')
            end_datetime = datetime.strptime(end_date, '%d/%m/%Y') if end_date else now

            await message.channel.send('Iniciando contagem de presença 🤓:\n\n'
                                       f'Data inicial: {start_date}\n'
                                       f'Data final: {end_date or now_formatted}')

            channels = self.client.get_all_channels()

            target_channel = discord.utils.get(channels, name='dia-de-office')

            message_history = target_channel.history(
                after=start_datetime, before=end_datetime)
            all_messages = [message async for message in message_history]

            weekdays = ['Segunda-feira', 'Terça-feira', 'Quarta-feira',
                        'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
            weekdays_or_expression = '|'.join(weekdays)
            day_format_expression = '([0-9]{2})/([0-9]{2})'

            pattern = re.compile(
                f'^({weekdays_or_expression}), {day_format_expression}:$')

            attendance_messages = list(
                filter(lambda message: pattern.match(message.content), all_messages))

            reactions = [
                reaction for message in attendance_messages for reaction in message.reactions]

            user_attendance_dict = {}

            for reaction in reactions:
                if reaction.emoji == '📍':
                    attended_users = [user async for user in reaction.users()]

                    for user in attended_users:
                        if user.id == self.client.user.id:
                            continue

                        if not user.name in user_attendance_dict:
                            user_attendance_dict[user.name] = 0

                        user_attendance_dict[user.name] += 1

            users_padded_by_ht = [
                f'{user}	{count}' for user, count in user_attendance_dict.items()]

            file_content = '\n'.join(users_padded_by_ht)

            file = discord.File(io.StringIO(file_content), 'attendance.txt')

            result_message = f'Total de mensagens: {len(attendance_messages)}\nResultado:'

            await message.channel.send(result_message, file=file)
