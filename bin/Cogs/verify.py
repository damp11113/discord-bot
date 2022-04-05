import time
import discord
from discord.ext import commands
from discord_slash import cog_ext
from damp11113.randoms import ranstr
from configobj import ConfigObj
import logging
from PIL import Image, ImageDraw
from damp11113.file import removefile

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = ConfigObj('../config.ini')


    @commands.command()
    async def vfy(self, ctx):
        vt = int(self.config.get('verify'))
        if vt == 1:
            img = Image.new('RGB', (100, 30), color = (73, 109, 137))
            d = ImageDraw.Draw(img)
            r = ranstr(10)
            d.text((10,10), r, fill=(255,255,0))
            img.save('verify.png')
            embed = discord.Embed(title='Verify', description='กรุณาพิมพ์ข้อความตามภาพเพื่อยืนยันตัวตน', color=0x00ff00)
            file = discord.File('verify.png', filename='verify.png')
            embed.set_image(url='attachment://verify.png')
            await ctx.send(file=file, embed=embed)
            c = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
            if c.content == r:
                await ctx.channel.purge(limit=2)
                await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name='notverify'))
                await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name='verify'), reason='Verified & AutoRole')
                emb = discord.Embed(title='Verify', description='ยืนยันตัวตนเรียบร้อยแล้ว', color=0x00ff00)
                await ctx.send(embed=emb)
                time.sleep(5)
                await ctx.channel.purge(limit=1)
                removefile('verify.png')
            else:
                await ctx.channel.purge(limit=2)
                embe = discord.Embed(title='Verify', description='ยืนยังไม่สำเร็จ', color=0xff0000)
                await ctx.send(embed=embe)
                time.sleep(5)
                await ctx.channel.purge(limit=1)
                removefile('verify.png')
        elif vt == 2:
            pawd = self.config.get('password')
            embed1 = discord.Embed(title='Verify', description='กรุณาพิมพ์รหัสผ่านเพื่อยืนยันตัวตน', color=0x00ff00)
            await ctx.send(embed=embed1)
            c = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
            if c.content == pawd:
                await ctx.channel.purge(limit=2)
                await ctx.author.remove_roles(discord.utils.get(ctx.guild.roles, name='notverify'))
                await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name='verify'), reason='Verified & AutoRole')
                embed2 = discord.Embed(title='Verify', description='ยืนยันตัวตนเรียบร้อยแล้ว', color=0x00ff00)
                await ctx.send(embed=embed2)
                time.sleep(5)
                await ctx.channel.purge(limit=1)
            else:
                await ctx.channel.purge(limit=2)
                embed3 = discord.Embed(title='Verify', description='ยืนยันตัวตนไม่สำเร็จ', color=0xff0000)
                await ctx.send(embed=embed3)
                time.sleep(5)
                await ctx.channel.purge(limit=1)
        elif self.config.get('verify') == 3:
            # question or introduce yourself
            embed2 = discord.Embed(title='Verify', description='ชื่ออะไร', color=0x00ff00)
            message = await ctx.send(embed=embed2)
            c = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
            await c.delete()
            embed3 = discord.Embed(title='Verify', description=f'คุณคือ {c.content}', color=0x00ff00)
            pass


        else:
            await ctx.send('การยืนยันปิดอยู่ กรุณาติดต่อผู้ดูแลระบบ')
            await ctx.channel.purge(limit=1)

def setup(bot):
    logging.info(f'loaded {__name__}')
    bot.add_cog(Verify(bot))