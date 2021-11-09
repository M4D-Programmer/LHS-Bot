import requests
import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
from itertools import cycle
import json
import logging
from datetime import datetime

global _version_
_version_ = "0.1.0"

global OPEN_DATE_ACTIVE
OPEN_DATE_ACTIVE = True
global DATE
DATE = "2021-11-12"

GUILD_ID = 831170627901587466

status = ['Magic 8Ball', 'Converter', 'CoinFlipper', 'Tic-Tac-Toe']

cogs_loaded = []
cogs_unloaded = []

Embed = discord.Embed()


def is_it_me(ctx):
    return ctx.author.id == 515364565245231114


def is_it_riley(ctx):
    return ctx.author.id == 502961134371078145

def get_prefix(client, message):
    if str(message.channel.type) == 'private':
        return str("!")
    else:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]


# Enable all intents except for members and presences
intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent.

client = commands.Bot(command_prefix=get_prefix, intents=intents)


@client.event
async def on_ready():
    check_date.start()
    print("Bot is online")
    #textChannels = discord.utils.get(client.guilds.channel)
    '''
    while True:
        print("type the channel then what you want to say")
        
        channel = client.get_channel(int(input()))
        bop = input("")
        await channel.send(bop)
        ''''''
        for server in client.servers:
            for channel in server.channels:
                if channel.name == 821548633051758653:
                    await client.send_message(channel, bop)
                    '''

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = '!'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    
    with open('WheelPresets.json', 'r') as f:
        WheelPresets = json.load(f)
    WheelPresets[str(guild.id)] = {'preset': '', 'options': ''}
    WheelPresets[str(guild.id)]['preset'] = f""
    WheelPresets[str(guild.id)]['options'] = f""
    with open('WheelPresets.json', 'w') as f:
        json.dump(WheelPresets, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    
    with open('WheelPresets.json', 'r') as f:
        WheelPresets = json.load(f)
    WheelPresets.pop(str(guild.id))
    with open('WheelPresets.json', 'w') as f:
        json.dump(WheelPresets, f, indent=4)
    print(f"LHS Bot has been removed from server {guild.id}")

@client.event
async def on_member_join(member):
    await member.send(f"Welcome to the LHS Server, {member.name}!\nPlease verify yourself by going to the verification channel and using the verify command. This is put in place to make sure we only have people from LHS in this server. (Plus there are a few bonuses that bot-dev's can tell you about)")
    '''
    global OPEN_DATE_ACTIVE
    server = client.get_guild(831170627901587466)
    if OPEN_DATE_ACTIVE == True:
        role = discord.utils.get(server.roles, name=f"{DATE}")
        await member.add_roles(role)
    else:
        pass'''

@client.event
async def on_member_remove(member):
    #print(f"{member} has been removed from the server")
    pass

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You can't do that.")
        await ctx.message.delete()
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter all the required arguments.")
        await ctx.message.delete()
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("That is not a recognized command.")
        await ctx.message.delete()
    elif isinstance(error, discord.errors.Forbidden):
        await ctx.send("You can't use that command in a DM.")
        await ctx.message.delete()
    elif isinstance(error, commands.CommandInvokeError):
        bot_dev = ctx.guild.get_member(515364565245231114)
        await ctx.send("Command error, the developer has been notified of the problem.")
        print(error)
        
        embed = discord.Embed(
            title="Error Detected",
            colour=ctx.author.colour,
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=ctx.author.avatar_url)
        fields = [("User", str(ctx.author), True),
                  ("Channel", ctx.channel, True),
                  ("Message", ctx.message.content, True),
                  ("Error", error, True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await bot_dev.send(embed=embed)

    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("You can't use that command in DMs.")
    else:
        raise error

@tasks.loop(minutes=30)
async def change_status():
    await client.change_presence(activity=discord.Game(random.choice(status)))
    # await client.change_presence(activity=discord.ActivityType(type=discord.ActivityType.listening, name="a song"))
    #await client.change_presence(activity=discord.ActivityType(type=discord.ActivityType.watching, name="a movie"))
    # await client.change_presence(activity=discord.Streaming(name="My Stream", url=""))


@tasks.loop(hours=1)
async def check_date():
    print("CHECKING DATE...")
    global OPEN_DATE_ACTIVE
    if OPEN_DATE_ACTIVE == True:
        date = datetime.now().date()
        print(date)
        print(DATE)
        if str(date) == DATE:
            server = client.get_guild(831170627901587466)
            role = server.get_role(894285516843937823) # HIDDEN ROLE #
            print("for")
            for member in server.members:
                await member.remove_roles(role)
            # GET HIDDEN ROLE AND REMOVE FROM ALL USERS #
            await role.edit(name=f"Hidden")
            print("edit")
            role = server.get_role(889967435288051755) # REGISTERED ROLE #
            #categories = ['SERVER INFO', 'SCHOOL ANNOUNCEMENTS', "TEXT CHANNELS", "HELP HOMEWORK", "VOICE CHANNELS"]
            print("for")
            for cat in server.categories:
                #category = discord.utils.get(server.categories, name=x)
                await cat.set_permissions(role, view_channel=True)
            print("done")
        # FIND A WAY TO SAVE WHO IS/ISNT REGISTERED OR CHANGE REGISTERED PERMS #
            OPEN_DATE_ACTIVE = False
        else:
            pass
    else:
        pass


@client.command(hidden=True)
@commands.check(is_it_me)
async def setstatus(ctx, stat, *, game=''):
    if stat == 'idle':
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(f"{game}"))
    else:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"{game}"))

@client.command(hidden=True)
@commands.check(is_it_me)
async def Clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

@client.command(hidden=True)
@commands.check(is_it_me)
async def load(ctx, extension):
    client.load_extension(f'Cogs.{extension}')
    cogs_loaded.append(extension)
    try:
        cogs_unloaded.remove(extension)
    except:
        pass
    await ctx.send(f"{extension} has been loaded")
    pass

@client.command(hidden=True)
@commands.check(is_it_me)
async def unload(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')
    cogs_unloaded.append(extension)
    try:
        cogs_loaded.remove(extension)
    except:
        pass
    await ctx.send(f"{extension} has been unloaded")

@client.command(hidden=True, aliases=['reload'])
@commands.check(is_it_me)
async def _reload(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')
    client.load_extension(f'Cogs.{extension}')
    await ctx.send(f"{extension} has been reloaded")

@client.command(hidden=True)
@commands.check(is_it_me)
async def showloaded(ctx):
    GUILD = ctx.guild
    print(GUILD)
    await ctx.send(f"""{str(cogs_loaded).replace("'",'')}""")

@client.command(hidden=True)
@commands.check(is_it_me)
async def showunloaded(ctx):
    await ctx.send(f"""{str(cogs_unloaded).replace("'",'')}""")

# CUSTOM COMMANDS #

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')
        cogs_loaded.append(filename[:-3])
    else:
        pass

@client.command(hidden=True)
@commands.check(is_it_me)
async def update(ctx):
    global _version_
    message = await ctx.send(f"Updating...")
    async with ctx.typing():
        try:
            for i in range(120):
                await asyncio.sleep(1)
                await message.edit(content=f"Waiting... [{120-i}]")
            await message.edit(content="[          ]")
            for filename in os.listdir('./Cogs'):
                if filename.endswith('.py'):
                    client.unload_extension(f'Cogs.{filename[:-3]}')
                    cogs_loaded.remove(filename[:-3])
            await message.edit(content="[█         ]")
            with requests.get("https://raw.githubusercontent.com/M4D-Programmer/LHS-Bot/main/__version__.py") as rq:
                with open('__version__.py', 'wb') as file:
                    file.write(rq.content)
                    file.close()
            await message.edit(content="[██        ]")
            x = 0
            from __version__ import author, version, Msg, Cogs
            print(f"Updatting from {_version_} to {version}")
            await ctx.send(f"Updatting from {_version_} to {version}")
            for Cog in Cogs:
                with requests.get(f"https://raw.githubusercontent.com/M4D-Programmer/LHS-Bot/main/Cogs/{Cog}.py") as rq:
                    with open(f'Cogs/{Cog}.py', 'wb') as file:
                        file.write(rq.content)
                        file.close()
                x += 1
                if x == 3:
                    await message.edit(content="[███       ]")
                if x == 6:
                    await message.edit(content="[████      ]")
                if x == 9:
                    await message.edit(content="[█████     ]")
                if x == 12:
                    await message.edit(content="[██████    ]")
            await message.edit(content="[███████   ]")
            if _version_ != version:
                _version_ = version
            await message.edit(content="[████████  ]")
            if Msg != "":
                channel = client.get_channel(893904274709422170)
                await channel.send(f"{Msg}")
            await message.edit(content="[█████████ ]")
            for filename in os.listdir('./Cogs'):
                if filename.endswith('.py'):
                    client.load_extension(f'Cogs.{filename[:-3]}')
                    cogs_loaded.append(filename[:-3])
            await message.edit(content="[██████████]")
                # RECV FILES IN COGS, CHECK DIFFERENCE (SERVER DOESN'T HAVE FILE THAT CLIENT DOES), REWRITE ALL FILES AND CREATE NEW ONES TO WRITE #
        except Exception as E:
            await ctx.send(f"{E}")

client.run('')

