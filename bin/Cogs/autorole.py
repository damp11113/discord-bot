import discord
from discord.ext import commands
from discord_slash import cog_ext
import logging
from discord_components import *
import time

class autorole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot)

    @commands.command()
    async def autorole(self, ctx):
        compo = [
             Select(
                 placeholder='เลือกยศ',
                 options=[
                     SelectOption(label='nsfw', value='nsfw')
                 ]
             )
        ]
        embed = discord.Embed(title='ยศที่จะเพิ่ม', description='กรุณาเลือกยศที่จะเพิ่มตามค้องการ', color=0x00ff00)
        message = await ctx.send(embed=embed, components=compo)
        interac = await self.bot.wait_for('select_option')
        if interac.option.value == 'nsfw':
            await ctx.channel.purge(limit=1)

            embed2 = discord.Embed(title='คุณอายุ 18+ ไหม', color=0x00ff00)
            compo2 = [
                Button(
                    label='ใช้',
                    custom_id='yes',
                    style=3
                ),
                Button(
                    label='ไม่ใช้',
                    custom_id='no',
                    style=4
                )
            ]
            await message.edit(embed=embed2, components=compo2)
            interac2 = await self.bot.wait_for("button_click")
            if interac2.custom_id == 'yes':
                await ctx.channel.purge(limit=1)
                role = discord.utils.get(ctx.guild.roles, name='nsfw')
                await ctx.author.add_roles(role)
                await message.edit(content='ยศที่คุณเพิ่มเรียบร้อยแล้ว')
                time.sleep(5)
                await message.delete()
            elif interac2.custom_id == 'no':
                await ctx.channel.purge(limit=1)


def setup(bot):
    bot.add_cog(autorole(bot))
    logging.info(f'{__name__} loaded')