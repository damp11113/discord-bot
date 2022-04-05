#!/bin/python3

# -------------------------------info--------------------------------------
"""
MIT License

Copyright (c) 2021 damp11113

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

___report___ = 'https://github.com/damp11113/discord-bot/issues'

version = 'V1.18.1 Dev'

build = '2022'

# -------------------------------import------------------------------------

import damp11113.check as sdk
import discord
import time
import os
import logging
from discord.ext import commands
from configobj import ConfigObj
from discord_slash import SlashCommand
from javascript import console
import platform
import damp11113.network as network
import sys
from keep_alive import keepalive

# ---------------------------------setup-1----------------------------------

config = ConfigObj('../config.ini')
OWNERID = config.get('OWNERID')

# ---------------------------------setup-2----------------------------------

intent = discord.Intents.all()
intent.members = True
intent.presences = True
bot = commands.Bot(command_prefix=config.get('command_prefix'), intents=intent)  # intent -> intents
bot.remove_command('help')
slash = SlashCommand(bot, sync_commands=True)

# ---------------------------------setup-3----------------------------------

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
_log_dt_fmt = '%Y-%m-%d %H:%M:%S'
_log_fmt = '[{asctime}] [{levelname}] {name}: {message}'
logging.basicConfig(format=_log_fmt, datefmt=_log_dt_fmt, style='{', level=logging.INFO)
logger = logging.getLogger('runner')
console.warn('starting')

# ---------------------------------setup-4----------------------------------

logger.info('get damp11113 info')
sdkver = sdk.info()
logger.info('check function use')
use = ['ranstr', 'createfolder', 'sizefolder', 'writefile', 'readfile', 'clock', 'removefile']
for i in use:
    if sdk.defcheck(i) == False:
        console.warn(f'{i} is not installed')
        sys.exit()
        
# ---------------------------------setup-5----------------------------------

keepalive()

# -------------------------------startup------------------------------------

@bot.event  # start
async def on_ready():
    os.system('title Booting up your system')
    await bot.change_presence(activity=discord.Game('%help - v1.17.1 DEV'))  # status
    os.system(f'title Ready - I am running on {bot.user.name} With the ID: {bot.user.id} - {version} Build {build} - {sdkver}')
    console.warn('-------------------------------------------------------------------')
    console.warn(f'| Ready')
    console.warn(f'| I am running on {bot.user.name}')
    console.warn(f'| ID {bot.user.id}')
    console.warn(f'| {version} Build {build}')
    console.warn(f'| Run on {platform.system()} {platform.release()}')
    console.warn(f'| SDK damp11113 - {sdkver}')
    console.warn(f'| issues: {___report___}')
    console.warn(f'| bot has support thai lang (beta) | บอทรองรับภาษาไทยแล้ว')
    console.warn(f'| translate by google/github')
    console.warn(f'| {str(len(bot.guilds))} servers | {str(len(bot.users))} users')
    console.warn('-------------------------------------------------------------------')


# ---------------------------------other commands--------------------------

@slash.slash(name="aboutbot", description="about your bot | เกี่วยกับบอท")
@commands.is_owner()
async def aboutbot(ctx):
    """about bot"""
    # show status, name, id, version, sdk, owner,  run_on, platfrom, lang
    embed = discord.embeds.Embed(title='name', description=f'{bot.user.name}', color=0x00ff00)
    embed.add_field(name='id', value=f'{bot.user.id}', inline=False)
    embed.add_field(name='version', value=f'{version}', inline=False)
    embed.add_field(name='sdk', value=sdkver, inline=False)
    embed.add_field(name='owner', value=f'{OWNERID}', inline=False)
    embed.add_field(name='run_on', value=f'{platform.system()} {platform.release()}', inline=False)
    embed.add_field(name='platform', value=f'python {sys.version}', inline=False)
    await ctx.send(embed=embed)


# -------------api------------------

@slash.slash(name="api", description="send api to url | ส่ง api ไปยัง url")
@commands.is_owner()
async def api(ctx, url):
    message = await ctx.send('waiting...')
    s = {
        'status': 'Ready',
        'name': bot.user.name,
        'id': bot.user.id,
        'version': f'{version} Build {build}',
        'sdk': f'damp11113 {sdkver}',
        'run_on': f'{platform.system()} {platform.release()}',
        'platform': f'python {sys.version}',
        'language': 'thai/eng'
    }
    st = network.sendtext(url, s)
    await message.edit(content=f'api sended status: {st}')

# --------------------------------event------------------------------------

@bot.event
async def on_guild_join(guild):
    # get system channel
    channel = guild.system_channel()
    if channel is not None:
        await channel.send(f'hello world! i an {bot.user.name}')
    else:
        console.warn(f'guild {guild.name} has no system channel')

@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(
        title='',
        color=discord.Color.red())
    embed1 = embed.add_field(name=f':x: Terminal Error', value=f"```{error}```")
    embed1.add_field(name="report bug",
                     value="<@735806290537873448> or %report or https://github.com/damp11113/discord-bot/issues",
                     inline=False)
    await ctx.send(embed=embed)
    os.system(f'title {error}')
    time.sleep(5)
    os.system(f'title Ready, I am running on {bot.user.name} With the ID: {bot.user.id}')
    raise error

# ---------------------------------cogs----------------------------

@slash.slash(name="load")
@commands.is_owner()
async def load(ctx, extension):
    # Check if the user running the command is actually the owner of the bot
    if ctx.author.id == OWNERID:
        bot.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Enabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")

# Unload command to manage our "Cogs" or extensions
@slash.slash(name="unload")
@commands.is_owner()
async def unload(ctx, extension):
    # Check if the user running the command is actually the owner of the bot
    if ctx.author.id == OWNERID:
        bot.unload_extension(f'Cogs.{extension}')
        await ctx.send(f"Disabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")

# Reload command to manage our "Cogs" or extensions
@slash.slash(name="reload")
@commands.is_owner()
async def reload_(ctx, extension):
    # Check if the user running the command is actually the owner of the bot
    if ctx.author.id == OWNERID:
        bot.reload_extension(f'Cogs.{extension}')
        await ctx.send(f"Reloaded the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")
        # Automatically load all the .py files in the Cogs folder

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'Cogs.{filename[:-3]}')
        except Exception:
            raise Exception

# ---------------------------------token---------------------------

bot.run(str(config.get('token')))
