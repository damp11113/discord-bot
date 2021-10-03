#!/bin/python3
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

import asyncio
import discord
from discord.ext import commands
import time
from time import sleep
import os
import sys
import random
import sqlite3
import click
import datetime
from gtts import gTTS
from tqdm import tqdm
import discordbotdash.dash as dbd
from notify import notification
from discord.ext.commands import bot
import logging
import contextlib
from logging . handlers import TimedRotatingFileHandler


os.system('title loading')

for i in tqdm(range(770)):
    sleep(0.001)


OWNERID = 735806290537873448
serverid = 820636278915465237
welcome = 831007898976780309
bot = commands.Bot(command_prefix='%')
global_filename = 'log.txt'
global_guildid = 0
password = 'sanswdw1714'
delay = 5
# Read the Data files and store them in a variable
TokenFile = open("./Token.txt", "r") # Make sure to paste the token in the txt file
TOKEN = TokenFile.read()
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
_log_dt_fmt = '%Y-%m-%d %H:%M:%S'
_log_fmt = '[{asctime}] [{levelname}] {name}: {message}'
logging.basicConfig(format=_log_fmt, datefmt=_log_dt_fmt, style='{', level=logging.INFO)
logger = logging.getLogger('runner')

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


@contextlib.contextmanager
def setup_logging(logfile=None, debug=False):
    try:
        logging.getLogger('discord').setLevel(logging.WARNING)
        logging.getLogger('discord.http').setLevel(logging.WARNING)

        log = logging.getLogger()
        log.setLevel(logging.INFO if not debug else logging.DEBUG)
        if logfile:
            handler = TimedRotatingFileHandler(filename=logfile, when='midnight', utc=True,
                                               encoding='utf-8', backupCount=5)
            fmt = logging.Formatter(_log_fmt, _log_dt_fmt, style='{')
            handler . setFormatter(fmt)
            log.addHandler(handler)
        else:
            logger.warning('Logging to file is disabled')

        yield
    finally:
        handlers = log.handlers[:]
        for  handler  in  handlers :
            handler.close()
            log.removeHandler(handler)

@bot.event# start
async def on_ready():
    os.system('title Booting up your system')
    await bot.change_presence(activity=discord.Game('starting'))  # status
    time.sleep(2)  # Sleep for 3 seconds
    await bot.change_presence(activity=discord.Game('starting.'))  # status
    time.sleep(1)  # Sleep for 3 seconds
    await bot.change_presence(activity=discord.Game('starting..'))  # status
    time.sleep(1)  # Sleep for 3 seconds
    await bot.change_presence(activity=discord.Game('starting...'))  # status
    time.sleep(2)  # Sleep for 3 seconds
    await bot.change_presence(activity=discord.Game('%help - v1.9'))  # status
    dbd.openDash(bot) # optional port: dbd.openDash(bot, port=5000)
    os.system(f'title Ready   I am running on {bot.user.name} With the ID: {bot.user.id}   V1.9  Build 1211')
    notification('Ready', title='bot')


@bot.command()
@commands.has_permissions(administrator=True)
async def clearall(ctx, amount=1000000):
 """clear all Message (admin only)"""
 if commands.has_permissions(manage_messages=True):
   await ctx.channel.purge(limit=amount)

@bot.command()
async def dm(ctx, member: discord.Member, *, content):
    """dm to user @(user)"""
    channel = await member.create_dm()
    await channel.send(content)

@bot.command()
async def aboutbot(ctx):
    """about bot"""
    embedVar = discord.Embed(title="Version", description="1.9", color=0x00ff00)
    embedVar.add_field(name="Build", value="1211", inline=False)
    embedVar.add_field(name="Name", value=bot.user.name, inline=False)
    embedVar.add_field(name="ID", value=bot.user.id, inline=False)
    await ctx.channel.send(embed=embedVar)

@bot.command()
async def givenum(ctx):

    # checks the author is responding in the same channel
    # and the message is able to be converted to a positive int
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and \
               msg.channel == ctx.channel

    await ctx.send("Type a number")
    msg1 = await bot.wait_for("message", check=check)
    await ctx.send("Type a second, larger number")
    msg2 = await bot.wait_for("message", check=check)
    x = int(msg1.content)
    y = int(msg2.content)
    if x < y:
        value = random.randint(x,y)
        await ctx.send(f"You got {value}.")
    else:
        await ctx.send(":warning: Please ensure the first number is smaller than the second number.")

@bot.command()
async def tts(ctx, language, *, speak):
    tts = gTTS(text=speak,lang=language)
    tts.save('speech.mp3')
    await ctx.send(file=discord.File(r'speech.mp3'))
    os.remove("speech.mp3")

@bot.command()
async def dmtts(ctx, language, member: discord.Member, *, speak):
    tts = gTTS(text=speak, lang=language)
    tts.save('speech1.mp3')
    channel = await member.create_dm()
    await channel.send(file=discord.File(r'speech1.mp3'))
    os.remove("speech1.mp3")

@bot.command()
async def timer(ctx, number:int):
    try:
        if number < 0:
            await ctx.send('number cant be a negative')
        elif number > 600:
            await ctx.send('number must be under 600')
        else:
            message = await ctx.send(number)
            while number != 0:
                number -= 1
                await message.edit(content=number)
                await asyncio.sleep(1)
            await message.edit(content='Ended!')
            await ctx.channel.purge(limit=2)

    except ValueError:
        await ctx.send('time was not a number')

@bot.command()
async def dmtimer(ctx, member: discord.Member, number:int):
    channel = await member.create_dm()
    try:
        if number < 0:
            await channel.send('number cant be a negative')
        elif number > 600:
            await channel.send('number must be under 600')
        else:
            message = await channel.send(number)
            while number != 0:
                number -= 1
                await message.edit(content=number)
                await asyncio.sleep(1)
            await message.edit(content='Ended!')


    except ValueError:
        await ctx.send('time was not a number')


@bot.command()
async def ping(message):
        """show the ping"""
        ping_ = bot.latency
        ping = round(ping_ * 1000)
        embedVar = discord.Embed(title="ping", description=f"my ping is {ping}ms", color=0x00ff00)
        await message.channel.send(embed=embedVar)

@bot.event
async def on_member_join(member):
    # Adds role to user
    # role = discord.utils.get(member.server.roles, name='Member')
    # await bot.add_roles(member, role)

    # Random embed color
    range = [255,0,0]
    rand = random.shuffle(range)

    # Welcomes User
    embed = discord.Embed(title="{}'s info".format(member.name), description="Welcome too {}".format(member.guild.name))
    embed.add_field(name="Name", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=member.status, inline=True)
    embed.add_field(name="Roles", value=member.top_role)
    embed.add_field(name="Joined", value=member.joined_at)
    embed.add_field(name="Created", value=member.created_at)
    embed.set_thumbnail(url=member.avatar_url)
    inlul = bot.get_channel(welcome)

    await inlul.send(inlul, embed=embed)

@bot.event
async def on_command_error(ctx,error):
    embed = discord.Embed(
    title='',
    color=discord.Color.red())
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.MissingPermissions):
        embed.add_field(name=f'Invalid Permissions', value=f'You dont have {error.missing_perms} permissions.')
        await ctx.send(embed=embed)
    else:
        embed1 = embed.add_field(name = f':x: Terminal Error', value = f"```{error}```")
        embed1.add_field(name="report bug", value="<@735806290537873448>", inline=False)
        await ctx.send(embed = embed)
        os.system(f'title {error}')
        notification(f"{error}", title='❌ Terminal Error')
        os.system(f'title Ready, I am running on {bot.user.name} With the ID: {bot.user.id}')
        # raise error



@bot.command()
async def load(ctx, extension):
    # Check if the user running the command is actually the owner of the bot
    if ctx.author.id == OWNERID:
        bot.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Enabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")


# Unload command to manage our "Cogs" or extensions
@bot.command()
async def unload(ctx, extension):
    # Check if the user running the command is actually the owner of the bot
    if ctx.author.id == OWNERID:
        bot.unload_extension(f'Cogs.{extension}')
        await ctx.send(f"Disabled the Cog!")
    else:
        await ctx.send(f"You are not cool enough to use this command")

# Reload command to manage our "Cogs" or extensions
@bot.command(name = "reload")
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



@click.command()
@click.option('--bot', '-B', default=False, is_flag=True)
@click.option('--token', '-t', default='')
@click.argument('guildid')
@click.argument('filename')
def main(bot, token, guildid, filename):
    global global_guildid, global_filename
    global_guildid = guildid
    global_filename = filename
    if token == '':
        try:
            bot.run(open('token.txt', 'r').read().split('\n')[0], bot=bot)
        except discord.errors.LoginFailure as e:
            os.system( f'title {e}, Try adding the `--bot` flag.')
            sleep(delay)
            os.system(f'title Ready, I am running on {bot.user.name} With the ID: {bot.user.id}')
    else:
        try:
            bot.run(token, bot=bot)
        except discord.errors.LoginFailure as e:
            os.system(f'title {e}, Try adding the `--bot` flag.')
            sleep(delay)
            os.system(f'title Ready, I am running on {bot.user.name} With the ID: {bot.user.id}')


async def make_logs():
    database = None

    def scrub(s):
        while "-" in s:
            s = s.replace("-", "")
        return s

    def check_table_exists(tablename):
        dbcur = database.cursor()
        dbcur.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='{0}';
            """.format(str(tablename).replace('\'', '\'\'')))
        if dbcur.fetchone():
            dbcur.close()
            return True

        dbcur.close()
        return False

    guild = bot.get_guild(int(global_guildid))
    database = sqlite3.connect("{}.sqlite".format(global_filename))

    cursor = database.cursor()
    if check_table_exists('channels'):
        cursor.execute("""DROP TABLE channels""")
    cursor.execute("""CREATE TABLE channels(cid INTEGER, position INTEGER, name TEXT, topic TEXT, type TEXT)""")
    cursor.close()
    database.commit()
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            cursor = database.cursor()
            cursor.execute(
                """INSERT INTO channels(cid, position, name, topic, type) VALUES (?, ?, ?, ?, ?)""",
                (channel.id, channel.position, channel.name, str(channel.topic), 'discord.TextChannel')
            )
            cursor.close()
            database.commit()
            if channel.permissions_for(guild.get_member(bot.user.id)).read_message_history:
                sys.stdout.write("Logging {0}: Counting".format(channel.name))
                sys.stdout.flush()
                cursor = database.cursor()
                after = datetime.datetime(2015, 3, 1)
                if check_table_exists(channel.id):
                    cursor.execute("""SELECT timestamp FROM `{0}` ORDER BY timestamp DESC LIMIT 1""".format(channel.id))
                    try:
                        after = datetime.datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d %H:%M:%S.%f")
                    except TypeError:
                        pass
                else:
                    cursor.execute(
                        """CREATE TABLE `{0}`(uid INTEGER, mid INTEGER, message TEXT, files TEXT, timestamp TEXT)""".format(
                            channel.id))
                database.commit()
                count = 0
                msg_c = 0
                async for message in channel.history(limit=None, after=after):
                    msg_c += 1
                print("\rLogging {0}: 0/{1}         ".format(channel.name, msg_c), end="")
                async for message in channel.history(limit=None, after=after):
                    at = ",".join([i.url for i in message.attachments])
                    cursor.execute("""
                        INSERT INTO `{0}`(uid, mid, message, files, timestamp)
                        VALUES (?, ?, ?, ?, ?)""".format(channel.id),
                                   (message.author.id, message.id, message.content, at, message.created_at))
                    count += 1
                    if count % 200 == 0:
                        database.commit()
                        print("\rLogging {0}: {1}/{2}".format(channel.name, count, msg_c), end="")
                database.commit()
                print("\rLogging {0}: [DONE]            ".format(channel.name))
        elif isinstance(channel, discord.VoiceChannel):
            cursor = database.cursor()
            cursor.execute(
                """INSERT INTO channels(cid, position, name, topic, type) VALUES (?, ?, ?, ?, ?)""",
                (channel.id, channel.position, channel.name, '', 'discord.VoiceChannel')
            )
            cursor.close()
            database.commit()
    print("LOGS FINISHED")
    os.system('title LOGS FINISHED')
    os.system('cls')
    sleep(delay)
    os.system(f'title Ready, I am running on {bot.user.name} With the ID: {bot.user.id}')



def get_embed(_title, _description, _color):
    return discord.Embed(title=_title, description=_description, color=_color)


@bot.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")


@bot.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")



def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

bot.run(str(TOKEN))  # token
