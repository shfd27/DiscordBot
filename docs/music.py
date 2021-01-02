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


    @commands.command(aliases=["stop"])
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
        import youtube_dl
        ytdl = youtube_dl.YoutubeDL(music_options.ytdl_options)
        raw_data=ytdl.extract_info(search, download=False)
        if "entries" in raw_data:   #search is not url
            raw_data=raw_data["entries"]
            if raw_data:
                raw_data=raw_data[0]
            else:
                self.bot.loop.create_task(ctx.send("No song detected for **"+str(search)+"**!"))
                return

        data={}
        data["extractor_key"]=raw_data["extractor_key"]
        if data["extractor_key"].startswith("Youtube"):
            keys=["url", "title", "webpage_url", "uploader", "uploader_url", "thumbnail", "duration", "upload_date", "channel_id"]
            for key in keys:
                data[key]=raw_data[key]
            data["duration"]=str(datetime.timedelta(seconds=data["duration"]))
            YOUTUBE_ID=raw_data['channel_id']
            url=f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={YOUTUBE_ID}&key={API_KEY}"
            api = urllib.request.urlopen(url).read()
            api=eval(str(api.decode("utf-8")))
            data["icon_url"]=api["items"][0]['snippet']['thumbnails']['high']['url']

        elif data["extractor_key"]=="TwitchStream":
            keys=["url", "description", "title", "webpage_url", "uploader", "uploader_id", "thumbnail"]
            for key in keys:
                data[key]=raw_data[key]
            if data["description"]!=None:
                data["title"]=data["description"]
            data["uploader_url"]="https://www.twitch.tv/"+str(data["uploader_id"])
            data["icon_url"]="https://github.com/shfd27/shfd27/blob/main/image/twitch.png?raw=true"
            data["duration"]="Live"

        elif data["extractor_key"]=="TwitchVod":
            keys=["url", "description", "title", "webpage_url", "uploader", "uploader_id", "thumbnail", "duration"]
            for key in keys:
                data[key]=raw_data[key]
            if data["description"]!=None:
                data["title"]=data["description"]
            data["uploader_url"]="https://www.twitch.tv/"+str(data["uploader_id"])
            data["icon_url"]="https://github.com/shfd27/shfd27/blob/main/image/twitch.png?raw=true"
            data["duration"]=str(datetime.timedelta(seconds=data["duration"]))
        
        elif data["extractor_key"]=="TwitchClips":
            keys=["url", "title", "webpage_url", "creator", "thumbnail", "duration", "uploader"]
            for key in keys:
                data[key]=raw_data[key]
            data["clip_uploader"]=data["uploader"]
            data["uploader"]=data["creator"]
            data["uploader_url"]=data["webpage_url"].split("/clip")[0]
            data["icon_url"]="https://github.com/shfd27/shfd27/blob/main/image/twitch.png?raw=true"
            data["duration"]=str(datetime.timedelta(seconds=data["duration"]))

        else:
            data["extractor_key"]=None
            data["url"]=raw_data["url"]
            data["title"]=raw_data["title"]
            if "duration" in raw_data:
                data["duration"]=raw_data["duration"]
            else:
                data["duration"]="Unknown"

        return data


    def play_embed(self, ctx):
        data=music_data[ctx.guild.id][0]
        if data["extractor_key"]!=None:
            embed=discord.Embed(title=data["title"], url=data["webpage_url"], color=0xfff0a7)
            embed.set_author(name=data["uploader"], url=data["uploader_url"], icon_url=data["icon_url"])
            embed.set_thumbnail(url=data["thumbnail"])
            embed.add_field(name="Duration", value=data["duration"], inline=True)
            embed.add_field(name="Requested by", value=ctx.author, inline=True)
            if data["extractor_key"]=="TwitchClips":
                embed.add_field(name="uploaded by", value=data["clip_uploader"], inline=False)
            embed.set_footer(text=str(data["extractor_key"])+" / "+str(ctx.author.voice.channel))
            return ctx.channel.send(embed=embed)
        else:
            embed=discord.Embed(title=data["title"], url=data["url"], color=0xfff0a7)
            embed.set_author(name="unkown", icon_url="https://github.com/shfd27/shfd27/blob/main/image/discord.png?raw=true")
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.add_field(name="Duration", value=data["duration"], inline=True)
            embed.add_field(name="Requested by", value=ctx.author, inline=True)
            embed.set_footer(text=str(ctx.author.voice.channel))
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
        if data==None:
            return
        if ctx.guild.id not in music_data.keys():
            music_data[ctx.guild.id]=[]
        if not music_data[ctx.guild.id]:
            source=discord.FFmpegPCMAudio(data["url"], before_options=music_options.before_options, options=music_options.options)
            source=discord.PCMVolumeTransformer(source, 0.5)
            ctx.voice_client.play(source, after=lambda s: self.play_after(ctx))
            music_data[ctx.guild.id].append(data)
            await self.play_embed(ctx)
        else:
            await ctx.send(f"Queuing **{data['title']}**!")
            music_data[ctx.guild.id].append(data)


    def play_after(self,ctx):
        if self.bot.user in ctx.message.author.voice.channel.members:
            if "volume" in music_data[ctx.guild.id][0]:
                volume=music_data[ctx.guild.id][0]["volume"]
            else:
                volume=0.5
            if "speed" in music_data[ctx.guild.id][0]:
                speed=music_data[ctx.guild.id][0]["speed"]
            else:
                speed=1.0
            music_data[ctx.guild.id].pop(0)
            if music_data[ctx.guild.id]:
                music_data[ctx.guild.id][0]["volume"]=volume
                music_data[ctx.guild.id][0]["speed"]=speed
                self.bot.loop.create_task(self.play_embed(ctx))
                source=discord.FFmpegPCMAudio(music_data[ctx.guild.id][0]["url"], before_options=music_options.before_options, options=music_options.options+" -filter:a atempo="+str(speed))
                source=discord.PCMVolumeTransformer(source, volume)
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


    @commands.command(aliases=["v","volume"])
    async def vol(self, ctx, volume: float):
        stat=self.check_stat(ctx)
        if stat==4:
            await ctx.send("You are not in voice_channel!")
        else:
            if stat==1:
                volume = volume / 100
                if volume>1.0:
                    await ctx.send("Volume should be less than **100**!")
                elif volume<=0.0:
                    await ctx.send("Volume should be above **0**!")
                else:
                    ctx.voice_client.source.volume = volume
                    await ctx.send("Change volume to **"+str(volume*100)+"**!")
                    music_data[ctx.guild.id][0]["volume"]=volume
            elif stat==2:
                await ctx.send("Bot is not in voice_channel!")
            elif stat==3:
                bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
                await ctx.send("You are not in **"+str(bot_class_Member.voice.channel)+"**!")


    @commands.command(aliases=["s"])
    async def speed(self, ctx, speed: float):
        stat=self.check_stat(ctx)
        if stat==4:
            await ctx.send("You are not in voice_channel!")
        else:
            if stat==1:
                if speed<=0.0:
                    await ctx.send("Speed should be above **0**!")
                else:
                    await ctx.send("Next song speed will be **"+str(speed)+"**!")
                    music_data[ctx.guild.id][0]["speed"]=speed
            elif stat==2:
                await ctx.send("Bot is not in voice_channel!")
            elif stat==3:
                bot_class_Member=ctx.guild.get_member_named(str(self.bot.user))
                await ctx.send("You are not in **"+str(bot_class_Member.voice.channel)+"**!")        



def setup(bot):
    bot.add_cog(Music(bot))