import discord
import asyncio
from discord.ext import commands
from configs import configs
import docs
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

#import configs
bot_name=configs.bot_name

TOKEN=configs.TOKEN
PREFIX=configs.PREFIX

bot = commands.Bot(command_prefix=PREFIX)


#import music module
bot.load_extension("docs.music")



@bot.event
async def on_ready():
    print(f"[Online] {bot.user}")
    activity = discord.Game(f"{PREFIX}help | {bot_name}")
    await bot.change_presence(status=discord.Status.online, activity=activity)




#run bot
bot.run(TOKEN)
