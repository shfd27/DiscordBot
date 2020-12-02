import discord
import asyncio
from discord.ext import commands
from discord.utils import get
from configs import configs
from docs import music_options
import urllib.request
import datetime

API_KEY = music_options.API_KEY
music_data={}


def search_to_data(search):
    data={}
    keys=["url", "webpage_url", "title", "uploader", "uploader_url", "thumbnail", "duration", "upload_date", "channel_id"]
    import youtube_dl
    ytdl = youtube_dl.YoutubeDL(music_options.ytdl_options)
    raw_data=ytdl.extract_info(search, download=False)
    if "entries" in raw_data:   #search is not url
        raw_data=raw_data["entries"][0]
    for key in keys:
        data[key]=raw_data[key]
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
        print(music_data)


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
            else:
                if self.bot.user not in channel.members:
                    bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
                    await ctx.message.channel.send("You are not in **"+str(bot_class_Member.voice.channel)+"**!")
                    raise commands.CommandError("Author is in another voice_channel...")
        else:
            await ctx.message.channel.send("You are not in voice_channel!")
            raise commands.CommandError("Author is not in voice_channel...")
        
        data=search_to_data(search)
        if ctx.guild.id not in music_data.keys():
            music_data[ctx.guild.id]=[]
        if not music_data[ctx.guild.id]:
            source=discord.FFmpegPCMAudio(data["url"], before_options=music_options.before_options, options=music_options.options)
            ctx.voice_client.play(source, after=lambda s: self.play_after(ctx))
            music_data[ctx.guild.id].append(data)
            await ctx.message.channel.send(f"Playing **{data['title']}**!")
        else:
            await ctx.message.channel.send(f"Queuing **{data['title']}**!")
            music_data[ctx.guild.id].append(data)


    def play_after(self,ctx):
        music_data[ctx.guild.id].pop(0)
        if music_data[ctx.guild.id]:
            self.bot.loop.create_task(ctx.message.channel.send(f"Playing **{music_data[ctx.guild.id][0]['title']}**!"))
            source=discord.FFmpegPCMAudio(music_data[ctx.guild.id][0]["url"], before_options=music_options.before_options, options=music_options.options)
            ctx.voice_client.play(source, after=lambda s: self.play_after(ctx))
        else:
            music_data[ctx.guild.id].clear()
            bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
            self.bot.loop.create_task("Leave from "+str(bot_class_Member.voice.channel)+"**!")
            self.bot.loop.create_task(ctx.voice_client.disconnect())



def setup(bot):
    bot.add_cog(Music(bot))