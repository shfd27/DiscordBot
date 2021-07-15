import asyncio
import datetime
import discord
import urllib.request

from configs import configs
from discord.ext import commands
from discord.utils import get
from discord_slash import cog_ext, SlashContext
from discord_slash.utils import manage_commands
from docs import music_options

#Import configs.
PREFIX=configs.PREFIX
bot_name=configs.bot_name
bot = commands.Bot(command_prefix=PREFIX)

class Info(commands.Cog, name="info"):
    def __init__(self,bot):
        self.bot=bot

    @cog_ext.cog_slash(
        name="invite",
        description="You can get the invite link!",
    )
    async def invite(ctx):
        url="https://discord.com/api/oauth2/authorize?client_id="+str(bot.user.id)+"&permissions=0&scope=bot"
        print(url)
        embed=discord.Embed(title="Invite Link", url=url, color=0xfff0a7)
        embed.set_thumbnail(url=bot.user.avatar_url)
        embed.add_field(name=f"Invite {bot_name}!", value=f"[「ㅤㅤㅤㅤ\nㅤInvite!ㅤ\nㅤㅤㅤㅤ」]({url})", inline=True)
        embed.set_footer(text=str(ctx.message.channel))
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Info(bot))