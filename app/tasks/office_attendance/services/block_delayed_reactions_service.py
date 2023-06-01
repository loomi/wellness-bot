from datetime import datetime
import os
import discord

DEADLINE_HOUR = 18
DEADLINE_MINUTE = 10
DEADLINE_SECOND = 00
DELAYED_EMOJI = '🕰️'

async def block_delayed_reaction_service(client: discord.Client, reaction: discord.RawReactionActionEvent):
    now = datetime.now()

    if reaction.channel_id != int(os.getenv('DIA_DE_OFFICE_CHANNEL_ID')):
        return

    curr_date = now.date()
    curr_time = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=now.hour,
        minute=now.minute,
        second=now.second
    )

    channel = client.get_channel(reaction.channel_id)
    message = await channel.fetch_message(reaction.message_id)

    message_date = datetime.date(message.created_at)
    deadline = datetime(
        year=message_date.year,
        month=message_date.month,
        day=message_date.day,
        hour=DEADLINE_HOUR,
        minute=DEADLINE_MINUTE,
        second=DEADLINE_SECOND
    )

    is_day_after_reaction = curr_date != message_date
    is_reaction_after_deadline = curr_time > deadline
    is_checkable_emoji = reaction.emoji.name == '📍'

    if is_checkable_emoji and (is_day_after_reaction or is_reaction_after_deadline):
        user = reaction.member
        await message.remove_reaction(emoji='📍', member=user)
        await reaction.member.send(
            f'Oiê, passando aqui porque você reagiu à mensagem de presença do dia **{message_date}** com {reaction.emoji} após o prazo estabelecido.\n\ndeadline: __*{message_date} {str(DEADLINE_HOUR).zfill(2)}:{str(DEADLINE_MINUTE).zfill(2)}:{str(DEADLINE_SECOND).zfill(2)}*__\nreação: __*{curr_date} {now.hour}:{now.minute}:{now.second}*__\n\nContudo, você ainda tem direito ao auxílio! Por favor, volte ao canal e reaja à mensagem daquele dia com {DELAYED_EMOJI}.\n_ps: removi tua reação tá 😉_')
