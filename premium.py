import mysql.connector
import discord
import logging
import damp11113.randoms
from discord.ext import commands
from discord_slash import cog_ext
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

sql = mysql.connector.connect(host="localhost", user="root", password="sanswdw1714", database="premium")

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dc = DiscordComponents(self.bot)

    @cog_ext.cog_slash(name="premium check", description='Check premium key | เช็คคีย์พรีเมียม')
    @commands.has_permissions(administrator=True)
    async def premium_check(self, ctx, key):
        message = await ctx.send(f"Checking key | กำลังเช็คคีย์")
        cursor = sql.cursor()
        cursor.execute("SELECT * FROM premium WHERE _key = '{}'".format(key))
        result = cursor.fetchone()
        if result is None:
            await message.edit(content="no key not found | ไม่พบคีย์พรีเมียมนี้")
        else:
            await message.edit(content="key found | พบคีย์พรีเมียมนี้")
            await ctx.send(f'Use key now? | ต้องการใช้คีย์นี้หรือไม่?',
                components=[
                    Button(label='Yes | ใช้เลย', style=ButtonStyle.green),
                    Button(label='No | ไม่ใช้', style=ButtonStyle.red)
                ])
            res = await self.bot.wait_for('button_click')
            if res.button.label == 'Yes | ใช้เลย':
                cursor.execute("UPDATE premium SET _used = 1 WHERE _key = '{}'".format(key))
                sql.commit()
                await message.edit(content="key used | ใช้คีย์พรีเมียมนี้แล้ว")
            elif res.button.label == 'No | ไม่ใช้':
                await message.edit(content="key not used | ไม่ใช้คีย์พรีเมียมนี้")

    @cog_ext.cog_slash(name='premium trial', description='Get premium trial | รับทดลองพรีเมียม')
    @commands.has_permissions(administrator=True)
    async def premium_trial(self, ctx):
        message = await ctx.send(f"Getting premium trial | กำลังรับทดลองพรีเมียม")
        key = damp11113.randoms.rankeygen(8, 8)
        cursor = sql.cursor()
        cursor.execute("INSERT INTO premium (_key, _used) VALUES ('{}', 0)".format(key))
        sql.commit()
        await message.edit(content="key generated | สร้างคีย์พรีเมียมแล้ว")
        await ctx.send(f'Key: {key} free trial 30 day | คีย์: {key} ทดลองพรีเมียม 30 วัน')
        await ctx.send(f'Use key now? | ต้องการใช้คีย์นี้หรือไม่?',
            components=[
                Button(label='Yes | ใช้เลย', style=ButtonStyle.green),
                Button(label='No | ไม่ใช้', style=ButtonStyle.red)
            ])
        res = await self.bot.wait_for('button_click')
        if res.button.label == 'Yes | ใช้เลย':
            # set key to expired
            cursor.execute("UPDATE premium SET _used = 1 WHERE _key = '{}'".format(key))
            sql.commit()
            await message.edit(content="key used | ใช้คีย์พรีเมียมนี้แล้ว")
        elif res.button.label == 'No | ไม่ใช้':
            await message.edit(content="key not used | ไม่ใช้คีย์พรีเมียมนี้")
            # delete key
            cursor.execute("DELETE FROM premium WHERE _key = '{}'".format(key))
            sql.commit()
            await message.edit(content="key deleted | ลบคีย์พรีเมียมนี้แล้ว")

def setup(bot):
    bot.add_cog(Premium(bot))
    logging.info(f"Loaded {__name__}")




