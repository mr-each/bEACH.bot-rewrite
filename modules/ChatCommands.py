import discord
from discord.ext import commands
import modules.Functions as fnc

localesign = 'RU'

# Getting locale text for replies
DBtext = fnc.load_locale('ChatCommands')

class ChatCommands:
    def __init__(self, bot):
        self.bot = bot

    # --------------- Command for clearing chat ---------------

    @commands.command(aliases=['clr'])
    async def clear(self, ctx, amount='1'):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        #await ctx.message.delete()
            
        try:
            int(amount)
        except ValueError:
            await ctx.message.delete()
            await ctx.send(DBtext[1], delete_after = 2) 
            return
        amount = int(amount)
        if ctx.author.guild_permissions.manage_messages is True:
            if 0 < amount < 100:                
                messages = []
                async for message in ctx.channel.history(limit = amount+1):
                    messages.append(message)
                await ctx.channel.delete_messages(messages)
                await ctx.send(DBtext[3].format(len(messages)-1), delete_after = 2)
            else:
                await ctx.message.delete()
                await ctx.send(DBtext[4], delete_after = 2)
        else:
            await ctx.send(DBtext[5], delete_after = 2)

    # --------------- Command for quoting messages ---------------

    @commands.command(aliases=['qt','move','mv'])
    async def quote(self, ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()

        try:
            chnlID, msgID = ctx.message.content.split()[1:]  # Getting channel and message ID of source message
        except Exception:
            await ctx.send(DBtext[6], delete_after = 2)
            return
        chnlID = fnc.clear_id(chnlID)  # Clearing channel ID from mention
        chnl_from = self.bot.get_channel(chnlID)
        if chnl_from is None:
            await ctx.send(DBtext[7], delete_after = 2)
            return
        try:
            found_message = await chnl_from.get_message(msgID)
        except discord.NotFound:
            await ctx.send(DBtext[8], delete_after = 2)
            return
        qtembed = discord.Embed(
            description = found_message.content,
            timestamp = found_message.created_at,
            color = discord.Color.blue()
        )
        qtembed.set_footer(text='#'+chnl_from.name)
        qtembed.set_author(name=found_message.author.name, icon_url=found_message.author.avatar_url)
        # Getting attachment url if exist
        if found_message.attachments != []:
            attch = found_message.attachments.pop().get('url')
            qtembed.set_image(url=attch)

        await ctx.send(embed=qtembed)

    # --------------- Event for making embedded messages ---------------

    async def on_message(self, message):
        if (message.author == self.bot.user) or isinstance(message.channel, discord.abc.PrivateChannel):
            return

        if message.content.startswith('>>'):
            await message.delete()
            if message.author.color == discord.Color(0x000000):
                clr = discord.Color.light_grey()
            else:
                clr = message.author.color
            embed = await fnc.newembed(self.bot, user_id=message.author.id, content=message.content[2:], color=clr)
            await message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(ChatCommands(bot))
