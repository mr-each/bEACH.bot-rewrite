import discord
from discord.ext import commands
import random
import modules.Functions as fnc

localesign = 'RU'

# Getting locale text for replies
DBtext = fnc.load_locale('UtilityCommands')

# Getting links
f = open('linklist.txt', encoding='utf-8')
linklist = f.read().splitlines()
f.close()

class UtilityCommands:
    def __init__(self, bot):
        self.bot = bot

    # --------------- Command for bullying someone ---------------

    @commands.command(aliases=['bly','bul'])
    async def bully(self, ctx, targetID=''):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        # Getting phrases for bullying
        bullying = fnc.load_bullying_phrases()
        
        if targetID == '':
            await ctx.send(DBtext[1], delete_after = 2)
        else:
            content = ctx.message.content.split(' ', 1).pop(1)
            num = random.randint(1,((len(bullying)-2)//2))
            bullyline = 'bly' + str(num)
            bullyauth = 'auth' + str(num)
            bullyembed = discord.Embed(
                description = bullying[bullyline],
                color = discord.Color.red()
            )
            bullyembed.set_thumbnail(url=linklist[1])
            bullyembed.set_footer(text = '— ' + bullying[bullyauth])

            await ctx.send(DBtext[2].format(content), embed=bullyembed)

    # --------------- Command for adding new bullying line ---------------

    @commands.command()
    async def addbull(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        
        try:
            content = ctx.message.content.split(' ', 1).pop(1)
        except Exception:
            await ctx.send(DBtext[3], delete_after = 2)
        if content == '':
            await ctx.send(DBtext[3], delete_after = 2)
        else:
            bullying = fnc.load_bullying_phrases()
            f = open('locale/bullying' + localesign + '.txt', 'a', encoding='utf-8')
            f.write('\nbly'+str((len(bullying)//2))+'+++'+content)
            f.write('\nauth'+str((len(bullying)//2))+'+++'+ctx.author.name)
            f.close()
            await ctx.send(DBtext[4], delete_after = 2)

    # --------------- Command for ragequitting  ---------------

    @commands.command(aliases=['rq'])
    async def ragequit(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        fnc.megumin_img(ctx.author.avatar_url)
        rqch = await ctx.guild.create_voice_channel('RageQuit')
        await ctx.author.edit(voice_channel = rqch)
        await rqch.delete()
        await ctx.send(DBtext[5].format(ctx.author.mention), file = discord.File('img/out.png'))

    # --------------- Command for getting personal Megumin image  ---------------

    @commands.command(aliases=['mgm'])
    async def megumin(self, ctx, targetID=''):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        if targetID == '':
            target = ctx.author
        else:
            targetID = fnc.clear_id(targetID)
            try:
                target = await self.bot.get_user_info(targetID)
            except discord.NotFound:
                await ctx.send(DBtext[6], delete_after = 2)
                return
        fnc.megumin_img(target.avatar_url)
        await ctx.author.send(DBtext[5].format(target.name), file = discord.File('img/out.png'))

    # --------------- LMGTFY command ---------------

    @commands.command(aliases=['ggl'])
    async def google(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        try:
            content = ctx.message.content.split(' ', 1).pop(1)
            targetID, search = content.split(' ', 1)
        except Exception:
            await ctx.send(DBtext[7], delete_after = 2)
            return
        try:
            await self.bot.get_user_info(fnc.clear_id(targetID))
        except discord.NotFound:
            await ctx.send(DBtext[6], delete_after = 2)
            return
        else:
            gglembed = discord.Embed(
                description=DBtext[9].format(ctx.author.name) + '\n' + DBtext[10] + '\n' + DBtext[11].format(search.replace(' ', '+')),
                color=discord.Color.teal()
            )
            gglembed.set_thumbnail(url=linklist[2])
            await ctx.send(DBtext[2].format(targetID), embed=gglembed)

def setup(bot):
    bot.add_cog(UtilityCommands(bot))
