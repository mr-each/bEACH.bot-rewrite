import discord
from discord.ext import commands
import modules.Functions as bot

localesign = 'RU'

# Getting locale text for replies
DBtext = bot.load_locale('RoleCommands')

class RoleCommands:
    def __init__(self, bot):
        self.bot = bot

    # --------------- Command for creating an achievement role ---------------

    @commands.command()
    async def crach(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        if ctx.author.guild_permissions.manage_roles is True:
            if ctx.message.content[9:] == '':
                await ctx.send(DBtext[1], delete_after = 2)
            else:
                role_name = ctx.message.content[9:]
                guild = ctx.guild
                await guild.create_role(name='⭐' + str(role_name) + '⭐', permissions=discord.Permissions.none(), color=discord.Color(0xddc90d), reason = DBtext[2])
                await ctx.send(DBtext[3].format(role_name), delete_after = 5)
        else:
            await ctx.send(DBtext[4], delete_after = 2)

def setup(bot):
    bot.add_cog(RoleCommands(bot))
