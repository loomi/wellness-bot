from config.discord_client import DiscordClient

class Application:
  discord_client = None

  def run(self):
    discord_client = DiscordClient()

    self.discord_client = discord_client.client

  def setup_tasks():
    pass