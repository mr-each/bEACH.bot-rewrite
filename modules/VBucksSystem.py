import discord
from discord.ext import commands
import json
import modules.Functions as fnc
import asyncio

localesign = 'RU'

# Getting locale text for replies
DBtext = fnc.load_locale('VBucksSystem')

class VBucksSystem:
    def __init__(self, bot):
        self.bot = bot

    # --------------- Daily vbusck giveaway ---------------
    
    @commands.command(aliases=[])
    #@commands.cooldown(1, 60*60*22, commands.BucketType.user)
    @commands.check(fnc.new_day_check)
    async def v_daily(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()
    
        with open('users.json', 'r') as f:
            users = json.load(f)
        amount = 5
        fnc.add_vbucks(users, ctx.guild, ctx.author, amount)
        emoji = discord.utils.get(self.bot.emojis, name = 'bEACH_vbucks')
        await ctx.send(DBtext[1].format(amount, emoji), delete_after = 2)
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)

    @v_daily.error
    async def v_daily_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            if isinstance(ctx.channel, discord.abc.PrivateChannel):
                return
            await ctx.message.delete()

            await ctx.send(DBtext[2], delete_after = 2)
            print('tomorrow')
        else:
            print('error [{}]'.format(error))

    @commands.command(aliases=[])
    async def v_give(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        guild = ctx.guild
        author = ctx.author
        # Checking command's arguments
        try:
            target, amount = ctx.message.content.split()[1:]
        except Exception:
            await ctx.send(DBtext[3], delete_after = 2)
            return
        user_id = fnc.clear_id(target)
        # Checking for user existence
        try:
            user = await self.bot.get_user_info(user_id)
        except Exception:
            await ctx.send(DBtext[4], delete_after = 2)
            return
        # Checking if target is message author
        if user == author:
            await ctx.send(DBtext[5], delete_after = 2)
            return
        # Checking for integer amount value
        try:
            int(amount)
        except Exception:
            await ctx.send(DBtext[6], delete_after = 2)
            return
        with open('users.json', 'r') as f:
            users = json.load(f)
        # Checking author's currency status
        if int(amount) > users[str(guild.id)][str(ctx.author.id)]['vbucks']:
            await ctx.send(DBtext[7], delete_after = 2)
            return
        # Checking if ammount is positive number
        if int(amount) < 1:
            await ctx.send(DBtext[8], delete_after = 2)
            return
        # Checking target existence in DB
        if not str(user.id) in users[str(guild.id)]:
            await ctx.send(DBtext[9], delete_after = 2)
            return

        fnc.add_vbucks(users, guild, author, int(amount)*(-1))
        fnc.add_vbucks(users, guild, user, int(amount))
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)

        emoji = discord.utils.get(self.bot.emojis, name = 'bEACH_vbucks')
        await ctx.send(DBtext[10].format(author.mention, int(amount), emoji, target), delete_after = 2)
        if user != self.bot.user:
            await user.send(DBtext[11].format(author.mention, int(amount), emoji, guild.name))

    # --------------- NAME ---------------
    
    @commands.command(aliases=[])
    async def v_info(self, ctx, target_id = ''):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        guild = ctx.message.guild
        with open('users.json', 'r') as f:
            users = json.load(f)

        if target_id == '':
            user = ctx.message.author
        else:
            content = ctx.message.content.split(' ', 1).pop(1)
            user_id = fnc.clear_id(content)
            if not str(user_id) in users[str(guild.id)]:
                await ctx.send(DBtext[12], delete_after = 2)
                return
            else:
                user = await self.bot.get_user_info(user_id)

        #Database update in case the user is not there
        if (not str(guild.id) in users) or (not str(user.id) in users[str(guild.id)]):
            fnc.update_data(users, ctx.message.guild, ctx.message.author)

        #Embed
        exp_needed = (((users[str(guild.id)][str(user.id)]['level']+1)**4)//5 + 1) * 5
        emoji = discord.utils.get(self.bot.emojis, name = 'bEACH_vbucks')
        infoembed = discord.Embed(
            description=
            DBtext[13].format(users[str(guild.id)][str(user.id)]['level']) + '\n' +
            DBtext[14].format(users[str(guild.id)][str(user.id)]['experience'],exp_needed) + '\n' +
            DBtext[15].format(users[str(guild.id)][str(user.id)]['vbucks'],emoji)
            ,
            color=discord.Color.dark_orange()
        )
        infoembed.set_author(name = user.display_name)
        infoembed.set_thumbnail(url = user.avatar_url)
        if ctx.guild.icon is None:
            icon = discord.Embed.Empty
        else:
            icon = DBtext[16].format(str(guild.id),guild.icon)
        infoembed.set_footer(text = DBtext[17].format(guild.name), icon_url = icon)
        
        msg = await ctx.send(embed = infoembed)
        await msg.add_reaction('❌')
        def check(reaction, user):
            return msg.id == reaction.message.id and str(reaction.emoji) == '❌'
        await asyncio.sleep(1)
        reaction, user = await self.bot.wait_for('reaction_add', check = check)
        await reaction.message.delete()

    
    # --------------- LEVEL ---------------
    # --------------- Add new member to users database ---------------
    
    async def on_member_join(self, member):
        if member.bot:
            return
        else:
            with open('users.json', 'r') as f:
                users = json.load(f)

            fnc.update_data(users, member.guild, member)
            
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4, sort_keys=True)

    # --------------- Giving EXP and LVL to user on message ---------------

    async def on_message(self, message):
        if message.author.bot or isinstance(message.channel, discord.abc.PrivateChannel):
            return

        ctx = await self.bot.get_context(message)
        if ctx.valid:
            pass
        else:
            with open('users.json', 'r') as f:
                users = json.load(f)

            fnc.update_data(users, message.guild, message.author)
            await fnc.spam_cooldown(self.bot, users, message)
            fnc.add_experience(users, message.guild, message.author, 5)
            await fnc.level_up(users, message.guild, message.channel, message.author)
            
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4, sort_keys=True)
    
def setup(bot):
    bot.add_cog(VBucksSystem(bot))