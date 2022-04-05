import discord
from discord.ext import commands
from discord_components import *
import logging

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

class wait(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            if after.channel.id == 943860238694629436:
                # get admin chat channel
                channel = self.bot.get_channel(956080457005531146)
                embed = discord.Embed(title=f'{member.name} ได้ขอเข้า admin voice', color=0x00ff00)
                m = await channel.send(embed=embed, components=comp)
                b = await self.bot.wait_for('button_click')
                if b.custom_id == 'ok':
                    embed = discord.Embed(title=f'{member.name} ได้รับอนุญาตให้เข้า admin voice', color=0x00ff00)
                    await m.edit(components=eomp, embed=embed)
                    adminvc = self.bot.get_channel(943783695133863967)
                    await member.move_to(adminvc)
                else:
                    embed = discord.Embed(title=f'{member.name} ไม่ได้รับอนุญาตให้เข้า admin voice', color=0xff0000)
                    await m.edit(components=eomp, embed=embed)
                    await member.move_to(None)
            else:
                return


def setup(bot):
    bot.add_cog(wait(bot))
    logging.info(f'loaded {__name__}')