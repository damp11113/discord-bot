import logging
import discord
import os
from gtts import gTTS
from discord_slash import cog_ext
from discord.ext import commands

class tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="tts", description="create text to speech | สร้างเสียงตามข้อความ")
    async def tts(self, ctx, language, *, speak, namefile=None):
        await ctx.send("waiting...")
        if namefile is None:
            tts = gTTS(text=speak,lang=language)
            tts.save('speech.mp3')
            await ctx.channel.purge(limit=1)
            await ctx.send(file=discord.File(r'speech.mp3'))
            os.remove("speech.mp3")

        else:
            tts = gTTS(text=speak,lang=language)
            tts.save(f'{namefile}.mp3')
            await ctx.channel.purge(limit=1)
            await ctx.send(file=discord.File(f'{namefile}.mp3'))
            os.remove(f'{namefile}.mp3')

    @cog_ext.cog_slash(name="ping", description="ping bot | ดูความเร็วของ bot")
    async def ping(self, ctx):
        """show the ping"""
        await ctx.send("waiting...")
        ping_ = self.bot.latency
        ping = round(ping_ * 1000)
        # remove ms
        await ctx.channel.purge(limit=1)
        if ping <= 100:
            embedVar = discord.Embed(title="pong!", description=f"🕒::⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ {ping}ms", color=0x00ff00)
            await ctx.send(embed=embedVar)
        elif ping >= 100:
            embedVar2 = discord.Embed(title="pong!", description=f"🕒::🟩⬜⬜⬜⬜⬜⬜⬜⬜⬜ {ping}ms", color=0x00ff00)
            await ctx.send(embed=embedVar2)
        elif ping >= 200:
            embedVar3 = discord.Embed(title="pong!", description=f"🕒::🟩🟩⬜⬜⬜⬜⬜⬜⬜ {ping}ms", color=0x00ff00)
            await ctx.send(embed=embedVar3)
        elif ping >= 300:
            embedVar4 = discord.Embed(title="pong!", description=f"🕒::🟩🟩🟩⬜⬜⬜⬜⬜⬜ {ping}ms", color=0x00ff00)
            await ctx.send(embed=embedVar4)
        elif ping >= 400:
            embedVar5 = discord.Embed(title="pong!", description=f"🕒::🟩🟩🟩🟩⬜⬜⬜⬜⬜ {ping}ms", color=0x00ff00)
            await ctx.send(embed=embedVar5)
        elif ping >= 500:
            embedVar6 = discord.Embed(title="pong!", description=f"🕒::🟩🟩🟩🟩🟨⬜⬜⬜⬜ {ping}ms", color=0x00ff00)
            await ctx.send(embed=embedVar6)
        elif ping >= 600:
            embedVar7 = discord.Embed(title="pong!", description=f"🕒::🟩🟩🟩🟩🟨🟨⬜⬜⬜ {ping}ms", color=0x00ff00)
            await ctx.send(embed=embedVar7)
        elif ping >= 700:
            embedVar8 = discord.Embed(title="pong!", description=f"🕒::🟩🟩🟩🟩🟨🟨🟨⬜⬜ {ping}ms", color=0x00ff00)
            await ctx.send(embed=embedVar8)
        elif ping >= 800:
            embedVar9 = discord.Embed(title="pong!", description=f"🕒::🟩🟩🟩🟩🟨🟨🟨🟥⬜ {ping}ms", color=0x00ff00)
            await ctx.send(embed=embedVar9)
        elif ping >= 900:
            embedVar0 = discord.Embed(title="pong!", description=f"🕒::🟩🟩🟩🟩🟨🟨🟨🟥🟥 {ping}ms", color=0x00ff00)
            await ctx.send(embed=embedVar0)
        elif ping >= 1000:
            embedVar11 = discord.Embed(title="pong!", description=f"🕒::MAX {ping}", color=0x00ff00)
            await ctx.send(embed=embedVar11)
        else:
            embedVar12 = discord.Embed(title="pong!", description=f"🕒:: Error", color=0xff0000)
            await ctx.send(embed=embedVar12)

def setup(bot):
    bot.add_cog(tools(bot))
    logging.info(f'loaded {__name__}')



