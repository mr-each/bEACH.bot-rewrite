import discord
from discord.ext import commands
import json
import modules.Functions as fnc

localesign = 'RU'

# Getting locale text for replies
DBtext = fnc.load_locale('OwnerCommands')

class OwnerCommands:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def update_db(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        guild = ctx.guild
        members = guild.members
        with open('users.json', 'r') as f:
            users = json.load(f)
        if not str(guild.id) in users:
            users[str(guild.id)] = {}
        for user in members:
            if user.bot is False:
                if str(user.id) in users[str(guild.id)]:
                    users[str(guild.id)][str(user.id)]['name'] = user.name
                    if not 'experience' in users[str(guild.id)][str(user.id)]:
                        users[str(guild.id)][str(user.id)]['experience'] = 0
                    if not 'level' in users[str(guild.id)][str(user.id)]:
                        users[str(guild.id)][str(user.id)]['level'] = 1
                    if not 'vbucks' in users[str(guild.id)][str(user.id)]:
                        users[str(guild.id)][str(user.id)]['vbucks'] = 0
                    if not 'cooldown' in users[str(guild.id)][str(user.id)]:
                        users[str(guild.id)][str(user.id)]['cooldown'] = 0
                    if not 'daily_day' in users[str(guild.id)][str(user.id)]:
                        users[str(guild.id)][str(user.id)]['daily_day'] = 0
                    
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)
        print('User database updated!')

    @commands.command()
    @commands.is_owner()
    async def change_bot_name(self, ctx, name):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        await ctx.me.edit(nick = name)

    @commands.command(aliases=['cnt'])
    @commands.is_owner()
    async def content(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()
        
        print(ctx.message.content)

    @commands.command(aliases=[])
    @commands.is_owner()
    async def find_user(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        target = ctx.message.content.split().pop(1)
        user_id = fnc.clear_id(target)
        user = await self.bot.get_user_info(user_id)

        embed = discord.Embed(description='id: {}\ncreated_at: {}'.format(user.id, user.created_at))
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=[])
    @commands.is_owner()
    async def vbucks_set(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()
        
        with open('users.json', 'r') as f:
            users = json.load(f)

        target, amount = ctx.message.content.split()[1:]
        user_id = fnc.clear_id(target)
        user = await self.bot.get_user_info(user_id)
        fnc.change_vbucks_amount(users, ctx.message.guild, user, int(amount))

        emoji = discord.utils.get(self.bot.emojis, name = 'bEACH_vbucks')
        await ctx.send("{}'s {} changed to **{}**{}".format(target, emoji, amount, emoji))

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)

    @commands.command(aliases=[])
    @commands.is_owner()
    async def vbucks_change(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()
        
        with open('users.json', 'r') as f:
            users = json.load(f)

        target, amount = ctx.message.content.split()[1:]
        user_id = fnc.clear_id(target)
        user = await self.bot.get_user_info(user_id)
        fnc.add_vbucks(users, ctx.message.guild, user, int(amount))

        emoji = discord.utils.get(self.bot.emojis, name = 'bEACH_vbucks')
        await ctx.send("{}'s {} changed by **{}**{}".format(target, emoji, amount, emoji))

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)

def setup(bot):
    bot.add_cog(OwnerCommands(bot))