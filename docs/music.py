import discord
import asyncio
from discord.ext import commands
from discord.utils import get
from configs import configs


class Music(commands.Cog, name="music"):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("Bot is working!")


    @commands.command()
    async def join(self, ctx):
        if ctx.message.author.voice!=None:
            bot_voice_client=get(self.bot.voice_clients, guild=ctx.guild)
            channel=ctx.message.author.voice.channel
            if bot_voice_client==None:
                await channel.connect()
                await ctx.message.channel.send("Join to channel **"+str(ctx.message.author.voice.channel)+"**!")
            else:
                if self.bot.user in channel.members:
                    await ctx.message.channel.send("You are already in channel **"+str(ctx.message.author.voice.channel)+"**!")
                else:
                    await bot_voice_client.move_to(ctx.message.author.voice.channel)
                    await ctx.message.channel.send("Move to channel **"+str(ctx.message.author.voice.channel)+"**!")
        else:
            await ctx.message.channel.send("You are not in voice_channel!")


    @commands.command()
    async def leave(self, ctx):
        if ctx.guild.voice_client!=None:
            await ctx.guild.voice_client.disconnect()
            await ctx.message.channel.send("Leave from channel **"+str(ctx.message.author.voice.channel)+"**!")
        else:
            await ctx.message.channel.send("You are not in voice_channel!")


def setup(bot):
    bot.add_cog(Music(bot))