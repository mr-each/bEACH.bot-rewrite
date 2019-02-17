import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import types
import modules.Functions as fnc

localesign = 'RU'

# Getting locale text for replies
DBtext = fnc.load_locale('RainbowCommands')

rainbow_flag = True
rrole = 'RAINBOW'

class RainbowCommands:
    def __init__(self, bot):
        self.bot = bot

    # --------------- Command for making RAINBOW role  ---------------

    @commands.command(pass_context=True, aliases=['r_mkrl'])
    async def r_makerole(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        if ctx.author.guild_permissions.manage_roles is True:
            existence_check = discord.utils.get(ctx.guild.roles, name=rrole)
            rolepos = discord.utils.get(ctx.guild.roles, name=ctx.me.name).position
            if existence_check is None:
                rainbow_role = await ctx.guild.create_role(name=rrole, permissions=discord.Permissions.none())
                await rainbow_role.edit(position = rolepos)
                await ctx.send(DBtext[1], delete_after = 2)
            else:
                await ctx.send(DBtext[2], delete_after = 2)
        else:
            await ctx.send(DBtext[3], delete_after = 2)

    # --------------- Command for giving RAINBOW role  ---------------

    @commands.command(pass_context=True, aliases=['r_gvrl'])
    async def r_giverole(self, ctx, targetID=''):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        if ctx.author.guild_permissions.manage_roles is True:
            if targetID == '':
                member = ctx.author
            else:
                user = await self.bot.get_user_info(fnc.clear_id(targetID))
                member = discord.utils.find(lambda m: m.name == user.name, ctx.message.guild.members)
            await member.add_roles(discord.utils.get(ctx.message.guild.roles, name=rrole))
        else:
            await ctx.send(DBtext[3], delete_after = 2)

    # --------------- Command to start RAINBOOMING  ---------------

    @commands.command(pass_context=True)
    async def r_start(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        if ctx.author.guild_permissions.ban_members is True:
            await ctx.send(DBtext[4], delete_after = 6)
            def check(m):
                return m.channel == ctx.channel and m.author != self.bot.user# m.content == 'Yes' and or m.content == 'Y' or m.content == 'yes' or m.content == 'y'
            try:
                msg = await self.bot.wait_for('message', check = check, timeout = 4)
                if msg.content == 'Yes' or msg.content == 'Y' or msg.content == 'yes' or msg.content == 'y':
                    await ctx.send(DBtext[5].format(ctx.message.author.mention))
                    rName = get(ctx.guild.roles, name=rrole)
                    cd = 0.1
                    a = 0
                    global rainbow_flag
                    if rainbow_flag is False:
                        rainbow_flag = True

                    # colorlist = [red > purple]
                    colorlist = [16711680, 16737536, 16776448, 4718337, 54015, 32255, 6750463, 0x2e3136]
                    '''
                    colorlist2 = [0x00FF00, 0x00FF1A, 0x00FF35, 0x00FF50, 0x00FF6B, 0x00FF86, 0x00FFA1, 0x00FFBB, 0x00FFD6,
                                    0x00FFF1, 0x00F1FF, 0x00D6FF, 0x00BBFF, 0x00A1FF, 0x0086FF, 0x006BFF, 0x0050FF, 0x0035FF,
                                    0x001AFF, 0x0000FF, 0x0000FF, 0x1A00FF, 0x3500FF, 0x5000FF, 0x6B00FF, 0x8600FF, 0xA100FF,
                                    0xBB00FF, 0xD600FF, 0xF100FF, 0xFF00F1, 0xFF00D6, 0xFF00BB, 0xFF00A1, 0xFF0086, 0xFF006B,
                                    0xFF0050, 0xFF0035, 0xFF001A, 0xFF0000, 0xFF0000, 0xFF1A00, 0xFF3500, 0xFF5000, 0xFF6B00,
                                    0xFF8600, 0xFFA100, 0xFFBB00, 0xFFD600, 0xFFF100, 0xF1FF00, 0xD6FF00, 0xBBFF00, 0xA1FF00,
                                    0x86FF00, 0x6BFF00, 0x50FF00, 0x35FF00, 0x1AFF00, ]
                    '''
                    while rainbow_flag:
                        if rainbow_flag is True:
                            a = a + 1
                            for i in range(len(colorlist)):
                                await rName.edit(color=discord.Color(colorlist[i]))
                                await asyncio.sleep(cd)
                        else:
                            return
                else:
                    await ctx.send(DBtext[6], delete_after = 2)
            except Exception:
                await ctx.send(DBtext[7], delete_after = 2)
        else:
            await ctx.send(DBtext[8], delete_after = 2)

    # --------------- Command to stop RAINBOOMING  ---------------

    @commands.command(pass_context=True, aliases=['stop'])
    async def r_stop(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        global rainbow_flag
        rainbow_flag = False
        await ctx.send(DBtext[9], delete_after = 2)

def setup(bot):
    bot.add_cog(RainbowCommands(bot))
