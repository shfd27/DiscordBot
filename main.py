import discord
import asyncio
from discord.ext import commands
from configs import configs
import docs
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# import configs
bot_name=configs.bot_name

TOKEN=configs.TOKEN
PREFIX=configs.PREFIX

bot = commands.Bot(command_prefix=PREFIX)


# import music module
bot.load_extension("docs.music")


@bot.command()
async def invite(ctx):
    url="https://discord.com/api/oauth2/authorize?client_id="+str(bot.user.id)+"&permissions=0&scope=bot"
    print(url)
    embed=discord.Embed(title="Invite Link", url=url, color=0xfff0a7)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name=f"Invite {bot_name}!", value=f"[「ㅤㅤㅤㅤ\nㅤInvite!ㅤ\nㅤㅤㅤㅤ」]({url})", inline=True)
    embed.set_footer(text=str(ctx.message.channel))
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f"[Online] {bot.user}")
    activity = discord.Game(f"{PREFIX}help | {bot_name}")
    await bot.change_presence(status=discord.Status.online, activity=activity)



# run bot
bot.run(TOKEN)