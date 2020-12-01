import discord
import asyncio
from discord.ext import commands
from discord.utils import get
from configs import configs
from docs import music_options


def search_to_data(search):
    import youtube_dl
    ytdl = youtube_dl.YoutubeDL(music_options.ytdl_options)
    data=ytdl.extract_info(search, download=False)
    data=data["entries"][0]
    return data


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
        bot_voice_client=get(self.bot.voice_clients, guild=ctx.guild)
        if bot_voice_client!=None:
            bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
            await ctx.guild.voice_client.disconnect()
            await ctx.message.channel.send("Leave from channel **"+str(bot_class_Member.voice.channel)+"**!")
        else:
            await ctx.message.channel.send("Bot is not in voice_channel!")

    @commands.command()
    async def play(self, ctx, *, search):
        if ctx.message.author.voice!=None:
            bot_voice_client=get(self.bot.voice_clients, guild=ctx.guild)
            channel=ctx.message.author.voice.channel
            if bot_voice_client==None:
                await channel.connect()
                await ctx.message.channel.send("Join to channel **"+str(ctx.message.author.voice.channel)+"**!")
            else:
                if self.bot.user not in channel.members:
                    bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
                    await ctx.message.channel.send("You are not in **"+str(bot_class_Member.voice.channel)+"**!")
                    raise commands.CommandError("Author is in another voice_channel...")
        else:
            await ctx.message.channel.send("You are not in voice_channel!")
            raise commands.CommandError("Author is not in voice_channel...")
        
        data=search_to_data(search)
        






def setup(bot):
    bot.add_cog(Music(bot))
