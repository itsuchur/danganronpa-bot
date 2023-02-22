import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

DISCORD_API_KEY = os.getenv("DISCORD_TOKEN")

initial_extensions = (
    'cogs.ask',
    'cogs.commands'
)

intents = discord.Intents.default()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=intents,
            command_prefix='!',
        )

    async def setup_hook(self):
      for extension in initial_extensions:
        try:
            await self.load_extension(extension)
            print(f"An extension {extension} successfully loaded.")
        except discord.ext.commands.ExtensionError as Error:
            print(f'Failed to load an extension {extension}. Error: {Error}.')

    async def on_ready(self):
      print("Bot's ready.")


bot = Bot()
bot.run(DISCORD_API_KEY)

# We still need to sync this tree somehow, but you can make a command as discussed already.