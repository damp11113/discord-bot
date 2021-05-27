import discord
from discord.ext import commands
import time
from time import sleep
import os
import sys
from notify import notification
import pyfiglet
import TenGiphPy

for i in range(101):
    sys.stdout.write('\r')
    sys.stdout.write("[%-10s] %d%%" % ('='*i, 1*i))
    sys.stdout.flush()
    sleep(0.05)

t = TenGiphPy.Tenor(token='8XIAZ4MR4G6G')
OWNERID = 735806290537873448
serverid = 820636278915465237
welcome = 831007898976780309

bot = commands.Bot(command_prefix='%')
# start
@bot.event
async def on_ready():
    print('Logged on as')# Ready
    await bot.change_presence(activity=discord.Game('starting'))  # status
    time.sleep(2)  # Sleep for 3 seconds
    await bot.change_presence(activity=discord.Game('starting.'))  # status
    time.sleep(1)  # Sleep for 3 seconds
    await bot.change_presence(activity=discord.Game('starting..'))  # status
    time.sleep(1)  # Sleep for 3 seconds
    await bot.change_presence(activity=discord.Game('starting...'))  # status
    time.sleep(2)  # Sleep for 3 seconds
    await bot.change_presence(activity=discord.Game('%help - v2.4.3B bot by damp'))  # status
    print('Ready')
    notification('Ready', title='bot')

@bot.command()
async def ver(ctx):
    await ctx.send('v2.4.3 beta')

@bot.command()
@commands.has_permissions(administrator=True)
async def clearall(ctx, amount=1000000):
 if commands.has_permissions(manage_messages=True):
   await ctx.channel.purge(limit=amount)


@bot.command()
async def clear(ctx, amount=5):
    if commands.has_permissions(manage_messages=True):
        await ctx.channel.purge(limit=amount)


@bot.command()
async def dm(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)

@bot.command()
@commands.has_permissions(administrator=True)
async def sendtonews(ctx, *,content):
    channel = bot.get_channel(#channel)
    await channel.send(content)

@bot.command()
@commands.is_owner()
async def shutdownbot(ctx):
    for i in range(101):
        sys.stdout.write('\r')
        sys.stdout.write("[%-10s] %d%%" % ('=' * i, 1 * i))
        sys.stdout.flush()
        sleep(0.05)
        print('shutdown...')
    await bot.change_presence(activity=discord.Game('shutdown'))  # status
    time.sleep(1)
    await bot.change_presence(activity=discord.Game('shutdown.'))  # status
    time.sleep(1)
    await bot.change_presence(activity=discord.Game('shutdown..'))  # status
    time.sleep(1)
    await bot.change_presence(activity=discord.Game('shutdown...'))  # status
    notification('bot is shutdown', title='bot')
    exit()

@bot.command(pass_context = True)
async def song(ctx):
    await ctx.send(file=discord.File(r'878e6fcb9326616cfcd4653679346533.mp3'))

@bot.command()
async def textart(ctx, *, content):
    ascii_banner = pyfiglet.figlet_format(content)#, *, content
    embedVar = discord.Embed(title="This is art", description=ascii_banner, color=0x00ff00)
    await ctx.send(embed=embedVar)#embed=embedVar

@bot.command()
async def dmtableflip(ctx, member: discord.Member):
    channel = await member.create_dm()
    await ctx.send("ok")
    await channel.send("(╯°□°）╯︵ ┻━┻")

@bot.command()
async def dmshrug(ctx, member: discord.Member):
    channel = await member.create_dm()
    await ctx.send("ok")
    await ctx.send("¯\_(ツ)_/¯")

@bot.command()
async def dmunflip(ctx, member: discord.Member):
    channel = await member.create_dm()
    await ctx.send("ok")
    await channel.send("┬─┬ ノ( ゜-゜ノ)")

@bot.command()
async def tableflip(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("(╯°□°）╯︵ ┻━┻")


@bot.command()
async def unflip(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("┬─┬ ノ( ゜-゜ノ)")

@bot.command()
async def shrug(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("\_(ツ)_/")

@bot.command()
async def ping(message):
        ping_ = bot.latency
        ping = round(ping_ * 1000)
        embedVar = discord.Embed(title="ping", description=f"my ping is {ping}ms", color=0x00ff00)
        await message.channel.send(embed=embedVar)

@bot.command()
async def tenor(ctx, *, content):
    await ctx.send(t.random(content))

@bot.command()
async def dmtenor(ctx, member: discord.Member, context):
    channel = await member.create_dm()
    await ctx.send("ok")
    await channel.send(t.random(context))


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
        embed.add_field(name = f':x: Terminal Error', value = f"```{error}```")
        await ctx.send(embed = embed)
        raise error

# Load command to manage our "Cogs" or extensions
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

@bot.event
async def on_member_join(ctx, *, member):
    channel = member.server.get_channel(welcome)
    fmt = 'Welcome to the {1.name} Discord server, {0.mention}'
    await ctx.send_message(channel, fmt.format(member, member.server))

@bot.event
async def on_member_remove(ctx, *, member):
    channel = member.server.get_channel(welcome)
    fmt = '{0.mention} has left/been kicked from the server.'
    await ctx.send_message(channel, fmt.format(member, member.server))


bot.run('token')
