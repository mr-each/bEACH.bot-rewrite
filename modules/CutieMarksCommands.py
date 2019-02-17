import discord
from discord.ext import commands
import modules.Functions as fnc

localesign = 'RU'

# Getting locale text for replies
DBtext = fnc.load_locale('CutieMarksCommands')

class CutieMarksCommands:
    def __init__(self, bot):
        self.bot = bot

    # --------------- Neboyan mark ---------------

    @commands.command(aliases=['nebayan','nebajan','nebojan','nb'])
    async def neboyan(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        embed = await fnc.cutiemark(self.bot, ctx.message, 144055353934348288, DBtext[1])
        await ctx.send(embed=embed)

    async def on_message(self, message):
        if (message.author == self.bot.user) or isinstance(message.channel, discord.abc.PrivateChannel):
            return
        
        words = message.content.lower().split()
        for word in words:
            if word == 'боян' or word == 'баян':
                embed = await fnc.cutiemark(self.bot, message, 144055353934348288, DBtext[1])
                await message.channel.send(embed=embed)
                return       
        
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        emoji = discord.utils.get(self.bot.emojis, name = 'boyan')
        if (reaction.count < 2) and (reaction.emoji == emoji):
            embed = await fnc.cutiemark(self.bot, reaction.message, 144055353934348288, DBtext[1])
            await channel.send(embed=embed)

    # --------------- TiTupoy mark ---------------

    @commands.command(aliases=['tt'])
    async def titupoy(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        embed = await fnc.cutiemark(self.bot, ctx.message, 135140855982981121, DBtext[2])
        await ctx.send(embed=embed)

    # --------------- TupaHeyt mark ---------------

    @commands.command(aliases=['th','hate'])
    async def tupaheyt(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        embed = await fnc.cutiemark(self.bot, ctx.message, 533991178245505024, DBtext[3])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CutieMarksCommands(bot))
