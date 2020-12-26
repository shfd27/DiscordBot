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


class Music(commands.Cog, name="music"):
    def __init__(self,bot):
        self.bot=bot


    @commands.command()
    async def test(self, ctx):
        await ctx.send("Bot is working!")


    def check_stat(self, ctx):
        if ctx.message.author.voice!=None:
            bot_voice_client=get(self.bot.voice_clients, guild=ctx.guild)
            channel=ctx.message.author.voice.channel
            if bot_voice_client==None:
                return 2
            else:
                if self.bot.user in channel.members:
                    return 1
                else:
                    return 3
        else:
            return 4


    @commands.command()
    async def join(self, ctx):
        stat=self.check_stat(ctx)
        if stat==4:
            await ctx.send("You are not in voice_channel!")
        else:
            channel=ctx.message.author.voice.channel
            if stat==1:
                await ctx.send("Bot is already in channel **"+str(channel)+"**!")
            elif stat==2:
                await channel.connect()
                await ctx.send("Join to channel **"+str(channel)+"**!")
            elif stat==3:
                bot_voice_client=get(self.bot.voice_clients, guild=ctx.guild)
                await bot_voice_client.move_to(channel)
                await ctx.send("Move to channel **"+str(channel)+"**!")


    @commands.command()
    async def leave(self, ctx):
        stat=self.check_stat(ctx)
        if stat==4:
            await ctx.send("You are not in voice_channel!")
        else:
            if stat==1:
                if ctx.guild.id in music_data:
                    if music_data[ctx.guild.id]:
                        music_data[ctx.guild.id].clear()
                bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
                await ctx.guild.voice_client.disconnect()
                await ctx.send("Leave from channel **"+str(bot_class_Member.voice.channel)+"**!")
            elif stat==2:
                await ctx.send("Bot is not in voice_channel!")
            elif stat==3:
                bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
                await ctx.send("You are not in **"+str(bot_class_Member.voice.channel)+"**!")


    def search_to_data(self, ctx, search):
        data={}
        keys=["url", "webpage_url", "title", "uploader", "uploader_url", "thumbnail", "duration", "upload_date", "channel_id"]
        import youtube_dl
        ytdl = youtube_dl.YoutubeDL(music_options.ytdl_options)
        raw_data=ytdl.extract_info(search, download=False)
        if "entries" in raw_data:   #search is not url
            raw_data=raw_data["entries"]
            if raw_data:
                raw_data=raw_data[0]
            else:
                self.bot.loop.create_task(ctx.send("No song detected for **"+str(search)+"**!"))
                raise Exception("No song from search...")
        for key in keys:
            data[key]=raw_data[key]
        return data


    def play_embed(self, ctx):
            data=music_data[ctx.guild.id][0]
            YOUTUBE_ID=data['channel_id']
            url=f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={YOUTUBE_ID}&key={API_KEY}"
            api = urllib.request.urlopen(url).read()
            api=eval(str(api.decode("utf-8")))
            embed=discord.Embed(title=data['title'], url=data['webpage_url'], color=0xfff0a7) #, description="이것은 Embed입니다."
            embed.set_author(name=data["uploader"], url=data['uploader_url'], icon_url=api["items"][0]['snippet']['thumbnails']['high']['url'])
            embed.set_thumbnail(url=data['thumbnail'])
            embed.add_field(name="Duration", value=str(datetime.timedelta(seconds=data['duration'])), inline=True)
            embed.add_field(name="Requested by", value=ctx.author, inline=True)
            embed.set_footer(text=ctx.author.voice.channel)
            return ctx.channel.send(embed=embed)


    @commands.command()
    async def play(self, ctx, *, search):
        stat=self.check_stat(ctx)
        if stat==4:
            await ctx.send("You are not in voice_channel!")
            return
        else:
            if stat==2:
                channel=ctx.message.author.voice.channel
                await channel.connect()
            if stat==3:
                bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
                await ctx.send("You are not in **"+str(bot_class_Member.voice.channel)+"**!")
                return
        
        data=self.search_to_data(ctx, search)
        if ctx.guild.id not in music_data.keys():
            music_data[ctx.guild.id]=[]
        if not music_data[ctx.guild.id]:
            source=discord.FFmpegPCMAudio(data["url"], before_options=music_options.before_options, options=music_options.options)
            ctx.voice_client.play(source, after=lambda s: self.play_after(ctx))
            music_data[ctx.guild.id].append(data)
            await self.play_embed(ctx)
        else:
            await ctx.send(f"Queuing **{data['title']}**!")
            music_data[ctx.guild.id].append(data)


    def play_after(self,ctx):
        if self.bot.user in ctx.message.author.voice.channel.members:
            music_data[ctx.guild.id].pop(0)
            if music_data[ctx.guild.id]:
                self.bot.loop.create_task(self.play_embed(ctx))
                source=discord.FFmpegPCMAudio(music_data[ctx.guild.id][0]["url"], before_options=music_options.before_options, options=music_options.options)
                ctx.voice_client.play(source, after=lambda s: self.play_after(ctx))
            else:
                music_data[ctx.guild.id].clear()
                bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
                self.bot.loop.create_task(ctx.send("Leave from channel **"+str(bot_class_Member.voice.channel)+"**!"))
                self.bot.loop.create_task(ctx.voice_client.disconnect())


    @commands.command()
    async def skip(self, ctx):
        stat=self.check_stat(ctx)
        if stat==4:
            await ctx.send("You are not in voice_channel!")
        else:
            if stat==1:
                if ctx.guild.id in music_data:
                    if music_data[ctx.guild.id]:
                        data=music_data[ctx.guild.id][0]
                        await ctx.message.channel.send("skip song **"+str(data["title"])+"**!")
                        ctx.voice_client.stop()
                    else:
                        await ctx.message.channel.send("Bot is not playing music!")
                else:
                    await ctx.message.channel.send("Bot is not playing music!")
            elif stat==2:
                await ctx.send("Bot is not in voice_channel!")
            elif stat==3:
                bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
                await ctx.send("You are not in **"+str(bot_class_Member.voice.channel)+"**!")


    @commands.command()
    async def pause(self, ctx):
        stat=self.check_stat(ctx)
        if stat==4:
            await ctx.send("You are not in voice_channel!")
        else:
            if stat==1:
                if ctx.guild.voice_client.is_playing():
                    data=music_data[ctx.guild.id][0]
                    await ctx.send("pause song **"+str(data["title"])+"**!")
                    bot_voice_client=get(self.bot.voice_clients, guild=ctx.guild)
                    bot_voice_client.pause()
                else:
                    await ctx.send("Bot is not playing song now!")
            elif stat==2:
                await ctx.send("Bot is not in voice_channel!")
            elif stat==3:
                bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
                await ctx.send("You are not in **"+str(bot_class_Member.voice.channel)+"**!")


    @commands.command()
    async def resume(self, ctx):
        stat=self.check_stat(ctx)
        if stat==4:
            await ctx.send("You are not in voice_channel!")
        else:
            if stat==1:
                if ctx.guild.voice_client.is_paused():
                    data=music_data[ctx.guild.id][0]
                    await ctx.send("resume song **"+str(data["title"])+"**!")
                    bot_voice_client=get(self.bot.voice_clients, guild=ctx.guild)
                    bot_voice_client.resume()
                else:
                    await ctx.send("Bot is not pausing song now!")
            elif stat==2:
                await ctx.send("Bot is not in voice_channel!")
            elif stat==3:
                bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
                await ctx.send("You are not in **"+str(bot_class_Member.voice.channel)+"**!")


    @commands.command(aliases=["q"])
    async def queue(self,ctx):
        if ctx.guild.id in music_data:
            if music_data[ctx.guild.id]:
                data=music_data[ctx.guild.id]
                await ctx.send("**QUEUE LIST**")
                titles=""
                for k in range(len(data)):
                    titles+=str(k)+". "+str(data[k]["title"])+"\n"
                await ctx.send("`"+titles+"`")
            else:
                await ctx.send("No song on queue!")
        else:
            await ctx.send("No song on queue!")



def setup(bot):
    bot.add_cog(Music(bot))