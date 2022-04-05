import damp11113
import discord
from discord.ext import commands
from discord_slash import cog_ext
import logging
from damp11113.file import readfile, writefile
from configobj import ConfigObj
from damp11113 import clock


class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = ConfigObj('../config.ini')

    # help command
    @cog_ext.cog_slash(name="help", description="show commands all | แสดงคำสั่งทั้งหมด")
    async def help(self, ctx):
        embed = discord.embeds.Embed(title='คำสั่งสำหรับใช้งานบอท', description='คำสั่งทั้งหมดที่สามารถใช้งานได้กับบอทนี้', color=0x00ff00)
        embed.add_field(name='คุณสามารถใช้คำสั่งต่างๆ', value='โดยพิมพ์ลงบนห้องข้อความในเซิร์ฟเวอร์', inline=False)
        embed.add_field(name='รายการ Prefix', value='สัญลักษณ์นำหน้าคำสั่งคือ % หรือ /', inline=False)
        await ctx.send(embed=embed)

    # blacklist message
    @commands.Cog.listener()
    async def on_message(self, message):
        loc = self.config.get('blacklist')
        loc2 = self.config.get('blacklistlink')
        blacklist = readfile(loc)
        blacklistlink = readfile(loc2)
        if message.author.bot:
            return
        elif message.content.startswith(self.config.get('command_prefix')):
            return
        elif message.content.startswith('/'):
            return
        elif message.content.startswith('<@'):
            return
        elif message.content.startswith('<#'):
            return
        elif message.content.startswith('https://') or message.content.startswith('http://'):
            if message.content in blacklistlink.split():
                await message.delete()
                embed = discord.embeds.Embed(title='ข้อความถูกลบแล้ว', description='ข้อความนี้ถูกลบแล้วจากระบบ', color=0xFFFF00)
                embed.add_field(name='ข้อความที่ถูกลบ', value=message.content, inline=False)
                embed.add_field(name='ข้อหา', value='blacklist link', inline=False)
                embed.set_footer(text='ข้อความถูกลบโดยบอทสำหรับผู้ดูแลระบบ ถ้าผิดพลาดกรุณาติดต่อผู้ดูแลระบบ')
                await message.author.send(embed=embed)
                writefile('../blacklist.log', f'[{clock()}] | name: {message.author.name} | id: {message.author.id} | message: {message.content} | reason blacklist link')
                return
        elif message.content in blacklist.split():
            await message.delete()
            embed = discord.embeds.Embed(title='ข้อความถูกลบแล้ว', description='ข้อความนี้ถูกลบแล้วจากระบบ', color=0xFFFF00)
            embed.add_field(name='ข้อความที่ถูกลบ', value=message.content, inline=False)
            embed.add_field(name='ข้อหา', value='blacklist message', inline=False)
            embed.set_footer(text='ข้อความถูกลบโดยบอทสำหรับผู้ดูแลระบบ ถ้าผิดพลาดกรุณาติดต่อผู้ดูแลระบบ')
            await message.author.send(embed=embed)
            writefile('../blacklist.log', f'[{clock()}] | name: {message.author.name} | id: {message.author.id} | message: {message.content} | reason blacklist message')
            return

    @cog_ext.cog_slash(name="addblacklist", description="add blacklist (message) | เพิ่มข้อความที่จะถูกลบ")
    @commands.has_permissions(administrator=True)
    async def addblacklist(self, ctx, *, message):
        try:
            loc = self.config.get('blacklist')
            writefile(loc, message)
            embed = discord.embeds.Embed(title='เพิ่มแลัว', description='ข้อความนี้ถูกเพิ่มแลัว', color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.embeds.Embed(title='เพิ่มไม่สำเร็จ', description=f'เพราะ {e}', color=0xff0000)
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="addblacklistlink", description="add blacklist (link) | เพิ่ม link ที่จะถูกลบ")
    @commands.has_permissions(administrator=True)
    async def addblacklistlink(self, ctx, *, link):
        try:
            loc = self.config.get('blacklistlink')
            writefile(loc, link)
            embed = discord.embeds.Embed(title='เพิ่มแลัว', description='ข้อความนี้ถูกเพิ่มแลัว', color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.embeds.Embed(title='เพิ่มไม่สำเร็จ', description=f'เพราะ {e}', color=0xff0000)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(message(bot))
    logging.info(f"loaded {__name__}")