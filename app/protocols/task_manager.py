import discord


class ITaskManager:
    async def setup(self, client: discord.Client):
        '''Sets up all of the tasks interactions with the client'''
