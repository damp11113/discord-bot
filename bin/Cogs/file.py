import discord
from discord.ext import commands
import logging
import time
import os
from damp11113.file import sizefolder, createfolder, removefile
from discord_components import *
import damp11113

comp = [
    Button(
        label="ตกลง",
        style=3,
        custom_id='ok'
    ),
    Button(
        label="ยกเลิก",
        style=4,
            custom_id='cancel'
    )
]

eomp = [
    Button(
        label="ตกลง",
        style=3,
        custom_id='ok',
        disabled=True

    ),
    Button(
        label="ยกเลิก",
        style=4,
        custom_id='cancel',
        disabled=True
    )
]


class file(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot)

    #@cog_ext.cog_slash(name="add_file", description="Add file to storage | เพิ่มไฟล์ในการเก็บข้อมูล")
    @commands.command()
    async def add(self, ctx):
        # get channel id
        os.chdir('../file')
        channel_id = ctx.channel.id
        # get file name

        def check_space(id):
            try:
                s = sizefolder(f'../file/{id}')
                if s > 120:
                    return True
                else:
                    return False
            except:
                return False
        user_id = ctx.author.id
        if channel_id == 944083425218940939:
            embed = discord.Embed(title="กรุณาใส่ไฟล์", description='กรุณาใส่ไฟล์ที่ต้องการอัพโหลด', color=0x00ff00)
            m = await ctx.send(embed=embed)
            # get file
            message = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if str(message.attachments) == '[]':
                return
            embed = discord.Embed(title="คุณต้องการอัพโหลดไฟล์นี้ใช่หรือไม่", color=0x00ff00)
            await m.edit(embed=embed, components=comp)
            inter = await self.bot.wait_for('button_click')
            await m.delete()
            if inter.custom_id == 'ok':
                mm = await ctx.send('กำลังอัพโหลดไฟล์')
                if check_space(user_id) is True:
                    await mm.edit(content='พื้นที่ไม่เพียงพอ')
                    await message.add_reaction('🟥')
                    time.sleep(3)
                    await mm.delete()
                else:
                    try:
                        await message.attachments[0].save(f'{user_id}/{message.attachments[0].filename}')
                        await mm.edit(content='อัพโหลดไฟล์เสร็จสิ้น')
                        await message.add_reaction('🟩')
                        time.sleep(3)
                        await mm.delete()
                    except:
                        createfolder(f'{user_id}')
                        await message.attachments[0].save(f'{user_id}/{message.attachments[0].filename}')
                        await mm.edit(content='อัพโหลดไฟล์เสร็จสิ้น')
                        await message.add_reaction('🟩')
                        time.sleep(3)
                        await mm.delete()
            else:
                a = await ctx.send('ยกเลิกการอัพโหลดไฟล์')
                await message.add_reaction('🟥')
                time.sleep(3)
                a.delete()
        else:
            m = await ctx.send("กรุณาใช้คำสั่งนี้ในห้อง <#944083425218940939>")
            time.sleep(5)
            await m.delete()

    @commands.command()
    async def space(self, ctx):
        # get channel id
        os.chdir('../file')
        channel_id = ctx.channel.id
        # get user id
        user_id = ctx.author.id
        user_name = ctx.author.name
        if channel_id == 944083425218940939:
            try:
                size = sizefolder(f'{user_id}')
                embed = discord.Embed(title=f"พื้นที่ของ {user_name}", color=0x00ff00)
                embed.add_field(name="ใช้ไป", value=f'{size} MB', inline=False)
                embed.add_field(name="เหลือ", value=f'{120 - size} MB', inline=False)
            except:
                createfolder(f'{user_id}')
                size = sizefolder(f'{user_id}')
                embed = discord.Embed(title=f"พื้นที่ของ {user_name}", color=0x00ff00)
                embed.add_field(name="ใช้ไป", value=f'{size} MB', inline=False)
                embed.add_field(name="เหลือ", value=f'{120 - size} MB', inline=False)
                embed.set_footer(text=f'สามารถขอพื้นที่เพิ่มจาก <@735806290537873448>')
            await ctx.send(embed=embed)
        else:
            m = await ctx.send("กรุณาใช้คำสั่งนี้ในห้อง <#944083425218940939>")
            time.sleep(5)
            await m.delete()

    @commands.command()
    async def delete(self, ctx):
        # get channel id
        os.chdir('../file')
        channel_id = ctx.channel.id
        # get user id
        user_id = ctx.author.id
        if channel_id == 944083425218940939:
            embed = discord.Embed(title="คุณต้องการลบไฟล์อะไร", color=0x00ff00)
            d = await ctx.send(embed=embed)
            ds = await self.bot.wait_for("message")
            embed = discord.Embed(title=f"คุณต้องการลบไฟล์ ใช่หรือไม่", description=ds, color=0x00ff00)
            await d.edit(embed=embed, components=comp)
            inter = await self.bot.wait_for('button_click')
            if inter.custom_id == 'ok':
                try:
                    removefile(f'{user_id}/{ds}')
                    await ctx.send(f'ลบไฟล์ {ds} เสร็จสิ้น')
                    await ds.add_reaction('🟩')
                except:
                    await d.delete()
                    embed = discord.Embed(title="ไม่พบไฟล์ที่ต้องการลบ", description=ds, color=0xff0000)
                    await ctx.send(embed=embed)
                    await ds.add_reaction('🟥')
            else:
                await d.delete()
                await ctx.send('ยกเลิกการลบไฟล์')
                await ds.add_reaction('🟥')
        else:
            m = await ctx.send("กรุณาใช้คำสั่งนี้ในห้อง <#944083425218940939>")
            time.sleep(5)
            await m.delete()

    @commands.command()
    async def list(self, ctx):
        os.chdir('../file')
        channel_id = ctx.channel.id
        # get user id
        user_id = ctx.author.id
        if channel_id == 944083425218940939:
            list = os.listdir(f'{user_id}')
            # dm to user id
            embed = discord.Embed(title=f"รายชื่อไฟล์ของ {ctx.author.name}", color=0x00ff00)
            embed.add_field(name='file', value=f'{damp11113.list2str(list)}')
            await ctx.send(embed=embed)
        else:
            m = await ctx.send("กรุณาใช้คำสั่งนี้ในห้อง <#944083425218940939>")
            time.sleep(5)
            await m.delete()

    @commands.command()
    async def download(self, ctx):
        os.chdir('../file')
        channel_id = ctx.channel.id
        # get user id
        user_id = ctx.author.id
        if channel_id == 944083425218940939:
            embed = discord.Embed(title="คุณต้องการดาวน์โหลดไฟล์อะไร", color=0x00ff00)
            d = await ctx.send(embed=embed)
            filename_ = await self.bot.wait_for('message')
            await d.delete()
            try:
                await ctx.send(file=discord.File(f'{user_id}/{filename_}'))
                await filename_.add_reaction('🟥')
            except:
                embed = discord.Embed(title="ไม่เจอไฟล์ที่คุณต้องการ", color=0xff0000)
                await ctx.send(embed=embed)
                await filename_.add_reaction('🟥')
        else:
            m = await ctx.send("กรุณาใช้คำสั่งนี้ในห้อง <#944083425218940939>")
            time.sleep(5)
            await m.delete()




def setup(bot):
    bot.add_cog(file(bot))
    logging.info(f"{__name__} loaded")