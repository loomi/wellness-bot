import discord


def get_target_channel(client: discord.Client):
    channels = client.get_all_channels()

    target_channel = discord.utils.get(channels, name='dia-de-office')

    return target_channel
