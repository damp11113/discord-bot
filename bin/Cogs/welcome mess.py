import discord
from discord.ext import commands
import logging
from configobj import ConfigObj


class WelcomeMess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = ConfigObj('../config.ini')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # add role to member with id
        # send message to member
        embed=discord.Embed(title=f'{member}', color=0x00ff00)
        embed.add_field(name=f'Welcome to {member.guild.name} Server', value=f'หย่าลืมอ่าน <#{self.config.get("rules")}>', inline=False)
        embed.add_field(name='Server', value='Invite Link: https://discord.gg/5bBCHcM4Jg', inline=False)
        embed.add_field(name="ถ้าโดนแบนสามารถยื่นคำขอรองได้ที่ https://forms.gle/zHVdGVtL8FoMN5Ld6", value='แต่ถ้ายื่นคำขอรองที่ไม่จริงจะโดนแบนหรือโดนแบนต่อโดยข้อหา ยื่นคำขอรองเท็จ', inline=False)
        embed.add_field(name="Owner", value='damp#5816', inline=False)
        embed.add_field(name="Administrator", value='Darkx090#8727', inline=False)
        embed.add_field(name="Developer", value='4wqw1r#2939', inline=False)
        embed.set_footer(text='ข้อมูลอาจมีความเป็นจริงหรือไม่ถูกต้อง กรุณาตรวจสอบข้อมูลอีกครั้ง จะเปลี่ยนแปลงทุกเดือน')
        await member.send(embed=embed)
        if self.config.get('verify') == '0':
            role1 = discord.utils.get(member.guild.roles, name='member')
            role2 = discord.utils.get(member.guild.roles, name='verify')
            await member.add_roles(role1)
            await member.add_roles(role2)
        else:
            role = discord.utils.get(member.guild.roles, name='notverify')
            await member.add_roles(role)

def setup(bot):
    bot.add_cog(WelcomeMess(bot))
    logging.info(f'loaded {__name__}')

