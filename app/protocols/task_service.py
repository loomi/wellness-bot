import discord


class ITaskService:
    client: discord.Client = None

    def __init__(self, client: discord.Client):
        self.client = client

    async def execute(self):
        '''Sets up all of the tasks interactions with the discord client'''
