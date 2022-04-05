import discord
from discord.ext import commands
import logging
from discord_slash import cog_ext
from damp11113.file import writefile
from damp11113.randoms import ranstr
from damp11113 import clock as date

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="kick", description="kick user | เตะผู้ใช้ออกจากเซิฟเวอร์")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send('waiting...')
        if reason is None:
            embedvar = discord.Embed(title='Kicked', description=f"You have been kicked from {ctx.guild.name}", color=0xff0000)
            embedvar.add_field(name='Reason', value='???')
            await member.send(embed=embedvar)
            await member.kick(reason=reason)
            await ctx.channel.purge(limit=1)
            embedVar = discord.Embed(title='Kicked', description=member.mention, color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            writefile('../kick.log', f'[{date("%z %A %d %B %Y  %p %H:%M:%S")}] | name {member.mention} | kick from {ctx.guild.name}')

        else:
            embedvar = discord.Embed(title='Kicked', description=f"You have been kicked from {ctx.guild.name}", color=0xff0000)
            embedvar.add_field(name='Reason', value=reason)
            await member.send(embed=embedvar)
            await member.kick(reason=reason)
            await ctx.channel.purge(limit=1)
            embedVar = discord.Embed(title='Kicked', description=member.mention, color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            writefile('../kick.log', f'[{date("%z %A %d %B %Y  %p %H:%M:%S")}] | name {member.mention} reason {reason} | kick from {ctx.guild.name}')

    @cog_ext.cog_slash(name="ban", description="ban user | แบนผู้ใช้ออกจากเซิฟเวอร์")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, time=None, reason=None):
        await ctx.send('waiting...')
        if time is None:
            ban_id = ranstr(10)
            embedvar = discord.embeds.Embed(title='Banned', description=f'You are temporarily banned for ------ from {ctx.guild.name} server!', color=0xff0000)
            embedvar.add_field(name='reason', value=reason)
            embedvar.add_field(name='Ban ID', value=ban_id)
            embedvar.set_footer(text=f'Sharing your Ban ID may affect the processing of your appeal!')
            writefile('../ban.log', f'[{date("%z %A %d %B %Y  %p %H:%M:%S")}] | name {member.mention} | ban_id {ban_id} reason {reason} | ban from {ctx.guild.name}')
            await member.send(embed=embedvar)
            await member.ban(reason=reason)
            await ctx.channel.purge(limit=1)
            embedVar = discord.Embed(title='Succeed', description=f"Banned {member.mention} reason {reason}", color=0x00ff00)
            await ctx.channel.send(embed=embedVar)

        if reason is None:
            ban_id = ranstr(10)
            embedvar = discord.embeds.Embed(title='Banned', description=f'You are temporarily banned for ------ from {ctx.guild.name} server!', color=0xff0000)
            embedvar.add_field(name='reason', value='???')
            embedvar.add_field(name='Ban ID', value=ban_id)
            embedvar.set_footer(text=f'Sharing your Ban ID may affect the processing of your appeal!')
            writefile('../ban.log', f'[{date("%z %A %d %B %Y  %p %H:%M:%S")}] | name {member.mention} | ban_id {ban_id}| ban from {ctx.guild.name}')
            await member.send(embed=embedvar)
            await member.ban()
            await ctx.channel.purge(limit=1)
            embedVar = discord.Embed(title='Succeed', description=f"Banned {member.mention} reason ???", color=0x00ff00)
            await ctx.channel.send(embed=embedVar)

        else:
            ban_id = ranstr(10)
            embedvar = discord.embeds.Embed(title='Banned', description=f'You are temporarily banned for {time} from {ctx.guild.name} server!', color=0xff0000)
            embedvar.add_field(name='reason', value=reason)
            embedvar.add_field(name='Ban ID', value=ban_id)
            embedvar.set_footer(text=f'You can use {ctx.prefix}unban {ban_id} to unban yourself')
            embedvar.set_footer(text=f'Sharing your Ban ID may affect the processing of your appeal!')
            writefile('../ban.log', f'[{date("%z %A %d %B %Y  %p %H:%M:%S")}] name {member.mention} | ban_id {ban_id} | reason {reason} | ban from {ctx.guild.name} | ban time {time}')
            await member.send(embed=embedvar)
            await member.ban(reason=reason, timeout=time)
            await ctx.channel.purge(limit=1)
            embedVar = discord.Embed(title='Succeed', description=f"Banned {member.mention} reason {reason}", color=0x00ff00)
            await ctx.channel.send(embed=embedVar)



    @cog_ext.cog_slash(name="unban", description="unban user | ยกเลิกการแบนผู้ใช้")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        await ctx.send('waiting...')
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.purge(limit=1)
                embedVar = discord.Embed(title='Succeed', description=f"Unbanned {user.mention}", color=0x00ff00)
                writefile('../ban.log', f'[{date("%z %A %d %B %Y  %p %H:%M:%S")}] | name {member} | unban from {ctx.guild.name}')
                await ctx.channel.send(embed=embedVar)
                return
        await ctx.channel.purge(limit=1)
        embedVar = discord.Embed(title='Error', description=f"Could not find {member}", color=0xff0000)
        await ctx.channel.send(embed=embedVar)

    @cog_ext.cog_slash(name="warn", description="warn user | เตือนผู้ใช้")
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send('waiting...')
        if reason is None:
            embedvar = discord.Embed(title='Warned', description=f"You have been warned from {ctx.guild.name} server", color=0xFFFF00)
            await member.send(embed=embedvar)
            await ctx.channel.purge(limit=1)
            embedVar = discord.Embed(title='Warned', description=f"{member.mention} has been warned.", color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            writefile('../warn.log', f'[{date("%z %A %d %B %Y  %p %H:%M:%S")}] | name {member.mention} | warn from {ctx.guild.name}')

        else:
            embedvar = discord.Embed(title='Warned', description=f"You have been warned from {ctx.guild.name} server", color=0xFFFF00)
            embedvar.add_field(name='Reason', value=reason)
            await member.send(embed=embedvar)
            await ctx.channel.purge(limit=1)
            embedVar = discord.Embed(title='Warned', description=f"{member.mention} has been warned. reason {reason}", color=0x00ff00)
            await ctx.channel.send(embed=embedVar)
            writefile('../warn.log', f'[{date("%z %A %d %B %Y  %p %H:%M:%S")}] | name {member.mention} | reason {reason} | warn from {ctx.guild.name}')

    @cog_ext.cog_slash(name="clear", description="clear messages | ลบข้อความ")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount):
        await ctx.send('waiting...')
        await ctx.channel.purge(limit=1)
        if amount == 'all':
            if commands.has_permissions(manage_messages=True):
                await ctx.channel.purge(limit=1000000)
                await ctx.send(f"cleared all messages")
        else:
            await ctx.channel.purge(limit=int(amount))
            await ctx.send(f"cleared {amount} messages")

    @cog_ext.cog_slash(name="lock", description='lock channel | ล็อคช่องสนทนา')
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx):
        await ctx.send('waiting...')
        overwrites = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrites.update(send_messages=False)
        await ctx.channel.edit(overwrites=overwrites)
        await ctx.channel.purge(limit=1)
        embedVar = discord.Embed(title='Locked', description=f"{ctx.channel.mention} has been locked", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        writefile('../lock.log', f'[{date("%z %A %d %B %Y  %p %H:%M:%S")}] | name {ctx.channel.mention} | locked from {ctx.guild.name}')

    @cog_ext.cog_slash(name="unlock", description='unlock channel | ปลดล็อคช่องสนทนา')
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx):
        await ctx.send('waiting...')
        overwrites = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrites.update(send_messages=True)
        await ctx.channel.edit(overwrites=overwrites)
        await ctx.channel.purge(limit=1)
        embedVar = discord.Embed(title='Unlocked', description=f"{ctx.channel.mention} has been unlocked", color=0x00ff00)
        await ctx.channel.send(embed=embedVar)
        writefile('../lock.log', f'[{date("%z %A %d %B %Y  %p %H:%M:%S")}] | name {ctx.channel.mention} | unlocked from {ctx.guild.name}')

def setup(bot):
    bot.add_cog(Admin(bot))
    logging.info(f"Loaded {__name__}")
