import asyncio
from discord.ext import commands
import discord
from gtts import gTTS
import os
import logging
from discord_slash import cog_ext, SlashContext


class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @cog_ext.cog_slash(name="dm", description="DM a user")
    async def dm(self, ctx, user: discord.Member, *, message):
        """DM a user"""
        messag = await ctx.send('sending...')
        await ctx.send('sending...')
        await user.send(message)
        await user.send(f'send from <@{ctx.author.id}>')
        await messag.edit(content=f'sented to {user.mention}')

    @cog_ext.cog_slash(name="dmrole", description="DM all users in a role")
    async def dmrole(self, ctx, role: discord.Role, *, message):
        """DM all users in a role"""
        messag = await ctx.send('sending...')
        for user in ctx.guild.members:
            if role in user.roles:
                await user.send(message)
                await user.send(f'send from <@{ctx.author.id}>')
        await messag.edit(content=f'sented to all users in {role.mention}')

    @cog_ext.cog_slash(name="dmall", description="DM all users in the server")
    async def dmall(self, ctx, *, message):
        """DM all users in the server"""
        messag = await ctx.send('sending...')
        for user in ctx.guild.members:
            await user.send(message)
            await user.send(f'send from <@{ctx.author.id}>')
        await ctx.channel.purge(limit=1)
        await messag.edit(content='sented to all users')


    @cog_ext.cog_slash(name="dmtts", description="DM a user with a text to speech")
    async def dmtts(self, ctx, language, member: discord.Member, *, speak, namefile=None):
        """DM a user with a text to speech"""
        messag = await ctx.send('waiting...')
        if namefile is None:
            tts = gTTS(text=speak,lang=language)
            tts.save('speech.mp3')
            await messag.edit(content='sending...')
            channel = await member.create_dm()
            await channel.send(f'send from <@{ctx.author.id}>')
            await channel.send(file=discord.File(r'speech.mp3'))
            os.remove("speech.mp3")
            await messag.edit(content=f'sented to {member.mention}')

        tts = gTTS(text=speak,lang=language)
        tts.save(f'{namefile}.mp3')
        await messag.edit(content='sending...')
        channel = await member.create_dm()
        await channel.send(f'send from <@{ctx.author.id}>')
        await channel.send(file=discord.File(f'{namefile}.mp3'))
        os.remove(f'{namefile}.mp3')
        await messag.edit(content=f'sented to {member.mention}')

    @cog_ext.cog_slash(name="dmroletts", description="DM all users in a role with a text to speech")
    async def dmroletts(self, ctx, language, role: discord.Role, *, speak, namefile=None):
        """DM all users in a role with a text to speech"""
        messag = await ctx.send('waiting...')
        if namefile is None:
            tts = gTTS(text=speak,lang=language)
            tts.save('speech.mp3')
            await messag.edit(content='sending...')
            for user in ctx.guild.members:
                if role in user.roles:
                    channel = await user.create_dm()
                    await channel.send(f'send from <@{ctx.author.id}>')
                    await channel.send(file=discord.File(r'speech.mp3'))
            os.remove("speech.mp3")
            await messag.edit(content=f'sented to all users in {role.mention}')

        tts = gTTS(text=speak,lang=language)
        tts.save(f'{namefile}.mp3')
        await messag.edit(content='sending...')
        for user in ctx.guild.members:
            if role in user.roles:
                channel = await user.create_dm()
                await channel.send(f'send from <@{ctx.author.id}>')
                await channel.send(file=discord.File(f'{namefile}.mp3'))
        os.remove(f'{namefile}.mp3')
        await messag.edit(content=f'sented to all users in {role.mention}')

    @cog_ext.cog_slash(name='dmalltts', description="DM all users in the server with a text to speech")
    async def dmalltts(self, ctx, language, *, speak, namefile=None):
        """DM all users in the server with a text to speech"""
        messag = await ctx.send('waiting...')
        if namefile is None:
            tts = gTTS(text=speak,lang=language)
            tts.save('speech.mp3')
            await messag.edit(content='sending...')
            for user in ctx.guild.members:
                channel = await user.create_dm()
                await channel.send(f'send from <@{ctx.author.id}>')
                await channel.send(file=discord.File(r'speech.mp3'))
            os.remove("speech.mp3")
            await messag.edit(content=f'sented to all users')

        tts = gTTS(text=speak,lang=language)
        tts.save(f'{namefile}.mp3')
        await messag.edit(content='sending...')
        for user in ctx.guild.members:
            channel = await user.create_dm()
            await channel.send(f'send from <@{ctx.author.id}>')
            await channel.send(file=discord.File(f'{namefile}.mp3'))
        os.remove(f'{namefile}.mp3')
        await messag.edit(content=f'sented to all users')


def setup(bot):
    bot.add_cog(DM(bot))
    logging.info(f"Loaded {__name__}")

