import discord
from discord.ext import commands
from discord_components import *
import logging
import time

# red = ready
# yellow = request
# blue = answer
# green = done
# orange = error/cancelled

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

class QandA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot)

    @commands.Cog.listener()
    async def on_message(self, message):
        # get message from 944112565011763251 (channel)
        if message.author.bot:
            pass
        elif message.channel.id == 944112565011763251:
            await message.add_reaction('🟥')
            embed = discord.Embed(title="คุณต้องการส่งคำถามไหม", colour=0x00ff00)
            m = await message.channel.send(embed=embed, components=comp)
            inter = await self.bot.wait_for('button_click')
            if inter.custom_id == 'ok':
                await m.edit(components=eomp)
                await m.edit(content="กำลังส่งคำถาม...")
                # get admin voice channel (943783695133863967)
                await message.add_reaction('🟨') # yellow
                # join voice channel
                # get admin channel (944142869340487680)
                qanr = self.bot.get_channel(944142869340487680)
                embed3 = discord.Embed(title="คำถามจากผู้ใช้", description=f'{message.author.name}', colour=0x00ff00)
                embed3.add_field(name="คำถาม", value=message.content, inline=False)
                embed3.set_footer(text=f"ส่งเมื่อ {time.strftime('%H:%M:%S')}")
                await m.delete()
                df = await qanr.send(embed=embed3, components=comp)
                inter3 = await self.bot.wait_for('button_click')
                await df.edit(components=eomp)
                if inter3.custom_id == 'ok':
                    await message.add_reaction('🟦') #blue
                    await qanr.send("พิมพ์คำตอบได้เลย")
                    # wait for message for channel
                    ar = await self.bot.wait_for('message')
                    embed3 = discord.Embed(title="คุณจะส่งคำตอบเลยไหม", colour=0xffff00)
                    om = await qanr.send(embed=embed3, components=comp)
                    inter3 = await self.bot.wait_for('button_click')
                    if inter3.custom_id == 'ok':
                        await om.edit(content="กำลังส่งคำตอบ...")
                        # reply message
                        # dm to user
                        embed6 = discord.Embed(title="คำถามของคุณถูกตอบแล้ว", description=f'จาก {ar.author.name}', colour=0x00ff00)
                        embed6.add_field(name="คำถามของคุณคือ", value=f'{message.content}', inline=False)
                        embed6.add_field(name="คำตอบ", value=ar.content, inline=False)
                        embed6.set_footer(text=f"ส่งเมื่อ {time.strftime('%H:%M:%S')}")
                        await message.author.send(embed=embed6)
                        await message.add_reaction('🟩')
                        await om.delete()
                        await ar.add_reaction('🟩')
                    elif inter3.custom_id == 'cancel':
                        embed6 = discord.Embed(title="คำถามของคุณถูกยกเลิก", description=f'กรุณาถามใหม่อีกครั้ง', colour=0xffff00)
                        await message.author.send(embed=embed6)
                        await message.add_reaction('🟧')
                elif inter3.custom_id == 'cancel':
                        embed6 = discord.Embed(title="คำถามของคุณถูกยกเลิก", description=f'กรุณาถามใหม่อีกครั้ง', colour=0xffff00)
                        await message.author.send(embed=embed6)
                        await message.add_reaction('🟧')
            elif inter.custom_id == 'cancel':
                await m.edit(content="ยกเลิกการส่งคำถามแล้ว")
                await message.add_reaction('🟧')
                time.sleep(2)
                await m.delete()

def setup(bot):
    bot.add_cog(QandA(bot))
    logging.info(f'{__name__} loaded')