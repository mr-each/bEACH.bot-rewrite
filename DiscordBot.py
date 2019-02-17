import discord
from discord.ext import commands
import modules.Functions as fnc
import json

localesign = 'RU'

# Reading TOKEN from file
config = fnc.load_config()
DBtoken = config['token']

# Getting locale text for replies
DBtext = fnc.load_locale('DiscordBot')

prefix = ['sr.', 'Sr.']

bot = commands.Bot(command_prefix = prefix)  # Command prefixes
bot.remove_command('help')  # Removing default HELP command

last_help_message = None

extensions = [
    'modules.ChatCommands',
    'modules.UtilityCommands',
    'modules.CutieMarksCommands',
    'modules.RoleCommands',
    'modules.RainbowCommands',
    'modules.VBucksSystem',
    'modules.OwnerCommands'
]

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print('Loaded {}'.format(extension))
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game(name='sr.help'))  # Giving custom status
        print('Connected!')
        print('Username: {}  ID: {}'.format(bot.user.name, bot.user.id))
        print('------')

    # --------------- Help command ---------------

    @bot.command()
    async def help(ctx):
        if isinstance(ctx.channel, discord.abc.PrivateChannel):
            return
        await ctx.message.delete()
        
        global last_help_message

        try:
            channel_id, message_id = config['last_help_message'][str(ctx.message.guild.id)]
            channel = bot.get_channel(channel_id)
            last_help_message = await channel.get_message(message_id)
            try:
                await last_help_message.delete()
            except Exception as error:
                print("Can't delete message [{}]".format(error))
        except Exception as error:
            print('There is no message [{}]'.format(error))

        value = fnc.load_help_commands('chat')
        helpembed = fnc.create_help(bot, f1=value) 
        msg = await ctx.send(embed=helpembed) 
        last_help_message = await msg.channel.get_message(msg.id)
        config['last_help_message'][str(msg.guild.id)] = [msg.channel.id, msg.id]
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4, sort_keys=True)

        vb_emoji = discord.utils.get(bot.emojis, name = 'bEACH_vbucks')
        emojis = ['💬','🇺','⭐', vb_emoji, '🦄', '🏳️‍🌈']
        for emoji in emojis:
            await last_help_message.add_reaction(emoji)

    @bot.event
    async def on_reaction_add(reaction, user):
        if user == bot.user:
            return
        
        guild = reaction.message.guild
        vb_emoji = discord.utils.get(bot.emojis, name = 'bEACH_vbucks')
        config = fnc.load_config()
        last_help_ch_id, last_help_m_id = config['last_help_message'][str(guild.id)]
        last_help_channel = guild.get_channel(last_help_ch_id)
        last_help_message = await last_help_channel.get_message(last_help_m_id)
        if reaction.message.id == last_help_message.id:
            await reaction.message.remove_reaction(reaction.emoji, user)
            # Chat commands
            if reaction.emoji == '💬':
                value = fnc.load_help_commands('chat')
                helpembed = fnc.create_help(bot, f1=value)
                await last_help_message.edit(embed=helpembed)
            # Util commands
            elif reaction.emoji == '🇺':
                value = fnc.load_help_commands('util')
                helpembed = fnc.create_help(bot, f2=value)
                await last_help_message.edit(embed=helpembed)
            # Role commands
            elif reaction.emoji == '⭐':
                value = fnc.load_help_commands('role')
                helpembed = fnc.create_help(bot, f3=value)
                await last_help_message.edit(embed=helpembed)
            # V-bucks commands
            elif reaction.emoji == vb_emoji:
                value = fnc.load_help_commands('vbucks')
                helpembed = fnc.create_help(bot, f4=value)
                await last_help_message.edit(embed=helpembed)
            # Cutie mark commands
            elif reaction.emoji == '🦄':
                value = fnc.load_help_commands('cutiemark')
                helpembed = fnc.create_help(bot, f5=value)
                await last_help_message.edit(embed=helpembed)
            # RAINBOW commands
            elif reaction.emoji == '🏳️‍🌈': 
                value = fnc.load_help_commands('rainbow')
                helpembed = fnc.create_help(bot, f6=value)
                await last_help_message.edit(embed=helpembed)
            else:
                return

    # --------------- Private message handler ---------------

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if isinstance(message.channel, discord.abc.PrivateChannel):
            await message.channel.send(DBtext[1])
            return

        await bot.process_commands(message)

    bot.run(DBtoken)