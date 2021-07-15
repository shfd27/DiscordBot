import asyncio
import discord
import discord_slash

from configs import configs
from discord.ext import commands
from discord_slash.utils import manage_commands

import docs
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

#import configs
TOKEN=configs.TOKEN
PREFIX=configs.PREFIX
bot_name=configs.bot_name
bot = commands.Bot(command_prefix=PREFIX)

#Slash Commands
slash = discord_slash.SlashCommand(bot, sync_commands=False)

# import music module/ Maybe changeable to for statement.
bot.load_extension("docs.music")
bot.load_extension("docs.info")

#When bot is invited, presence will appear.
@bot.event
async def on_guild_join():
    print(f"[Online] {bot.user}")
    activity = discord.Game(f"{PREFIX}help | {bot_name}")
    await bot.change_presence(status=discord.Status.online, activity=activity)

#When bot is loaded, presence will appear.
@bot.event
async def on_ready():
    print(f"[Online] {bot.user}")
    activity = discord.Game(f"{PREFIX}help | {bot_name}")
    await bot.change_presence(status=discord.Status.online, activity=activity)

# run bot
bot.run(TOKEN)