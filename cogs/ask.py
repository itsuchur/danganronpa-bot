import discord
from discord import app_commands
from discord.ext import commands

class Ask(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    
  @app_commands.command(name="askmonokuma")
  async def askmonokuma(self, interaction: discord.Interaction, question: str) -> None:
    await interaction.response.send_message("Hello from command 1!", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Ask(bot))