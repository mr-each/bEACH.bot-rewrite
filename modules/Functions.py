import discord
import asyncio
from PIL import Image, ImageDraw, ImageOps
import requests
from io import BytesIO
import json
from datetime import datetime, time, timedelta
import pytz

#import random
#from discord.ext import commands
#from discord.utils import get

localesign = 'RU'

# --------------- File loading ---------------

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

config = load_config()

def load_locale(module_name):
    f = open('locale/DBtext'+localesign+'/'+module_name, encoding='utf-8')
    bot_locale = ['null']
    bot_locale.extend(f.read().splitlines())
    f.close()
    return bot_locale

DBtext = load_locale('Functions')

def load_help_list():
    with open('locale/helpRU.json', 'r', encoding='utf-8') as f:
        help_list = json.load(f)
    return help_list

def load_help_commands(segment):
    with open('locale/helpRU.json', 'r', encoding='utf-8') as f:
        help_list = json.load(f)
    string = ''
    for cmd in help_list[segment+'-cmd']:
        string += cmd
    return string

def load_bullying_phrases():
    bullying_phrases = {}
    with open('locale/bullying'+localesign+'.txt', encoding='utf-8') as file:
        for line in file:
            key, value = line.split('+++')
            value = value.replace('\n', '')
            bullying_phrases[key] = value
    return bullying_phrases

# --------------- Clearing Channel and User IDs ---------------

def clear_id(clear_id):
    clear_id = clear_id.replace('<', '').replace('#', '').replace('@', '').replace('!', '').replace('>', '')
    clear_int_id = int(clear_id)
    return clear_int_id

# --------------- New embed generation ---------------

async def newembed(bot, user_id, content, color):
    user = await bot.get_user_info(user_id)

    newembed = discord.Embed(
        description=content,
        color=color
    )
    newembed.set_author(name=user.name, icon_url=user.avatar_url)
    return newembed

# --------------- New embed generation for cutiemark ---------------

async def cutiemark(bot, message, memberid, text):
    memid = memberid
    member = message.guild.get_member(memid)
    if member is None:
        clr = discord.Color.darker_grey()
    else:
        if member.color == discord.Color(0x000000):
            clr = discord.Color.light_grey()
        else:
            clr = member.color
    embed = await newembed(bot, user_id=memid, content=text, color = clr)
    return embed

# --------------- Short help generation ---------------

def create_help(bot, f1=DBtext[1], f2=DBtext[2], f3=DBtext[3], f4=DBtext[4], f5=DBtext[5], f6=DBtext[6]):
        helplist = load_help_list()
        embed = discord.Embed(
            description = helplist['prefix'],
            color = discord.Color.green()
        )
        embed.set_author(name = helplist['title'], icon_url = bot.user.avatar_url)
        embed.add_field(inline=False, name=helplist['chat'],  # Chat commands
                            value = f1)
        embed.add_field(inline=False, name=helplist['util'],  # Util commands
                            value = f2)
        embed.add_field(inline=False, name=helplist['role'],  # Role commands
                            value = f3)
        embed.add_field(inline=False, name=helplist['vbucks'],  # V-bucks commands
                            value = f4)
        embed.add_field(inline=False, name=helplist['cutiemark'],  # Cutie mark commands
                            value = f5)
        embed.add_field(name=helplist['rainbow'], inline=False,  # RAINBOW commands
                            value = f6)
        return embed

# --------------- Ragequit image ---------------

def megumin_img(url):
    # IMAGE generation
    size = 250, 250
    response = requests.get(url)
    avt = Image.open(BytesIO(response.content))
    avt = avt.resize(size, Image.ANTIALIAS)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0)+size, fill = 255)
    output = ImageOps.fit(avt, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    offset = (250, 285)
    mgm = Image.open('img/megu.png', 'r')
    mgm.paste(output, offset, output)
    mgm.save('img/out.png')

# --------------- Database update ---------------

def update_data(users_list, guild, user):
    if not str(guild.id) in users_list:
        users_list[str(guild.id)] = {}
    if not str(user.id) in users_list[str(guild.id)]:
        users_list[str(guild.id)][str(user.id)] = {}
        users_list[str(guild.id)][str(user.id)]['name'] = user.name
        users_list[str(guild.id)][str(user.id)]['experience'] = 0
        users_list[str(guild.id)][str(user.id)]['level'] = 1
        users_list[str(guild.id)][str(user.id)]['vbucks'] = 0
        users_list[str(guild.id)][str(user.id)]['cooldown'] = 0

# --------------- Level ---------------

def add_experience(users_list, guild, user, exp):
    if users_list[str(guild.id)][str(user.id)]['cooldown'] == 0:
        users_list[str(guild.id)][str(user.id)]['experience'] += exp
    else:
        cooldown_check = datetime.utcnow() - timedelta(seconds = 30) # For how long the cooldown will be
        if users_list[str(guild.id)][str(user.id)]['cooldown'] < int(cooldown_check.timestamp()):
            users_list[str(guild.id)][str(user.id)]['cooldown'] = 0
            users_list[str(guild.id)][str(user.id)]['experience'] += exp

async def level_up(users_list, guild, channel, user):
    experience = users_list[str(guild.id)][str(user.id)]['experience']
    lvl_start = users_list[str(guild.id)][str(user.id)]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        users_list[str(guild.id)][str(user.id)]['level'] = lvl_end
        users_list[str(guild.id)][str(user.id)]['experience'] = 0
        vbucks_coef = (lvl_end*5) - 5
        users_list[str(guild.id)][str(user.id)]['vbucks'] += vbucks_coef*5
        await channel.send(DBtext[7].format(user.mention, lvl_end), delete_after = 5)

async def spam_cooldown(client, users, message):
    timestamp = datetime.utcnow() - timedelta(seconds=30) # Time period for messages
    guild = message.guild
    user = message.author
    counter = 0
    async for log_message in message.channel.history(after = timestamp):
        if log_message.author == user:
            counter += 1
    if counter > 10 and users[str(guild.id)][str(user.id)]['cooldown'] == 0: # How many messages triggers cooldown
        users[str(guild.id)][str(user.id)]['cooldown'] = int(message.created_at.timestamp())
        await message.channel.send(DBtext[8].format(message.author.mention), delete_after = 5)
        
# --------------- V-Bucks ---------------

def add_vbucks(users_list, guild, user, vbucks):
    users_list[str(guild.id)][str(user.id)]['vbucks'] += vbucks

def change_vbucks_amount(users_list, guild, user, vbucks):
    users_list[str(guild.id)][str(user.id)]['vbucks'] = vbucks

def new_day_check(ctx):
    with open('users.json', 'r') as f:
        users = json.load(f)
    guild = ctx.guild
    user = ctx.author
    moscowtz = pytz.timezone('Europe/Moscow')
    if users[str(guild.id)][str(user.id)]['daily_day'] == datetime.now(tz = moscowtz).day:
        return False
    else:
        users[str(guild.id)][str(user.id)]['daily_day'] = datetime.now(tz = moscowtz).day
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4, sort_keys=True)
        return True
