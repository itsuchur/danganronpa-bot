from discord.ext import commands

class Commands(commands.Cog):
    __slots__ = ('bot')

    def __init__(self, bot):
        self.bot = bot
        self.tree = self.bot.tree

    @commands.command(hidden=True)
    @commands.guild_only()
    async def sync_all(self, ctx):
        if ctx.author.id == 173477542823460864:
            cmds = await self.bot.tree.sync()
            print(cmds)
            await ctx.send("✅")

    @commands.command(hidden=True)
    @commands.guild_only()
    async def sync_guild(self, ctx):
        if ctx.author.id == 173477542823460864:
            await self.bot.tree.sync(guild=ctx.guild)
            await ctx.send("✅")

async def setup(bot):
    await bot.add_cog(Commands(bot))