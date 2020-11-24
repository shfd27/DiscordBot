import discord
import asyncio
from discord.ext import commands
from configs import configs


class Music(commands.Cog, name="music"):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Bot is Online!")


def setup(bot):
    bot.add_cog(Music(bot))
