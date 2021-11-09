import discord
from discord.ext import commands
from colour import Color
from discord import Color as col
import asyncio

global Role_Message_ID
from _variables_ import Role_Message_ID

global GUILD
GUILD = None
global COLORS
COLORS = []
global ROLES_ACTIVE
ROLES_ACTIVE = True
global CUSTOM_COLORS_ALLOWED
CUSTOM_COLORS_ALLOWED = False

class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message:str):
        #print('Bot is online')
        if not ROLES_ACTIVE:
            return
        #print(GUILD.roles)
        if str(message.channel.name) == 'roles':
            if message.author.id == 694589350733807666:
                return
            #print(message.content)
            await asyncio.sleep(2)
            await message.delete()
        else:
            pass
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id == 694589350733807666:
            return
        #print("Channel")
        Channel = self.client.get_channel(831180525724368937)
        #print("Got Channel")
        if reaction.message.channel.id == Channel:
            #print("Returned")
            return
        else:
            if reaction.message.id != Role_Messaeg_ID:
                return
            if reaction.emoji == "🐦":
                role = discord.utils.get(user.guild.roles, name="Tweet Alerts")
                await user.add_roles(role)
            elif reaction.emoji == "🔔":
                role = discord.utils.get(user.guild.roles, name="Bell_Alerts")
                await user.add_roles(role)
            elif reaction.emoji == "🚍":
                role = discord.utils.get(user.guild.roles, name="Bus_Alerts")
                await user.add_roles(role)
            elif reaction.emoji == "📰":
                role = discord.utils.get(user.guild.roles, name="News Alerts")
                await user.add_roles(role)
    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.id == 694589350733807666:
            return
        #print("Channel")
        Channel = self.client.get_channel(831180525724368937)
        #print("Got Channel")
        if reaction.message.channel.id == Channel:
            #print("Returned")
            return
        else:
            if reaction.message.id != Role_Messaeg_ID:
                return
            if reaction.emoji == "🐦":
                role = discord.utils.get(user.guild.roles, name="Tweet Alerts")
                await user.remove_roles(role)  # PUT IN ON_REACTION_REMOVE
            elif reaction.emoji == "🔔":
                role = discord.utils.get(user.guild.roles, name="Bell_Alerts")
                await user.remove_roles(role)
            elif reaction.emoji == "🚍":
                role = discord.utils.get(user.guild.roles, name="Bus_Alerts")
                await user.remove_roles(role)
            elif reaction.emoji == "📰":
                role = discord.utils.get(user.guild.roles, name="News Alerts")
                await user.remove_roles(role)
    
    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def roles(self, ctx):
        message = await ctx.channel.send("""`SELECT A COLOR FOR A COLORED ROLE`\n\nblack\nred\norange\nyellow\ngreen\nblue\nviolet\nmagenta\nwhite\ncyan\nlime\n
Type !color `colorname` **IN THIS CHANNEL** to receive the appropriate color role
To remove the color, just do the same command, !color `colorname`
EXAMPLE: !color black

To get alerted for Mr. Burre's tweets(🐦), Bell changes(🔔), Bus changes(🚍), or school news(📰) react to this message.""")
        await message.add_reaction('🐦')
        await message.add_reaction('🔔')
        await message.add_reaction('🚍')
        await message.add_reaction('📰')
    
    @commands.command(aliases=['colour'])
    @commands.has_permissions()
    async def color(self, ctx, NAME):
        if not ROLES_ACTIVE:
            return
        
        global GUILD
        GUILD = ctx.guild
        #print(GUILD)
        if str(ctx.channel.name) == 'roles':
            #print(NAME)
            #print(GUILD.roles)
            for r in GUILD.roles:
                #print(r.name)
                try:
                    c = Color(r.name)
                    #print(c)
                    COLORS.append(r.name)
                except:
                    #print("is not a color")
                    pass
            try:
                c = Color(NAME)
            except:
                await ctx.send(f"That is not a color.")
                #print("is not a color")
                return
            
            try:
                try:
                    role = discord.utils.get(GUILD.roles, name=NAME)
                    #print(f"{role} role found")
                except:
                    #print("role can not be found")
                    c = Color(str(NAME))
                    await GUILD.create_role(name=c, colour=col.from_rgb(float(c.Red), float(c.Green), float(c.Blue)))
                    #print("Role created")
                user = ctx.author
                #print(user)
                if role in user.roles:
                    await user.remove_roles(role)
                else:
                    await user.add_roles(role)
                    #print("Role added to user")
            except Exception as e:
                await ctx.send(f"ERROR finding this role. Bot devs have been informed.")
                bot_dev = ctx.guild.get_member(515364565245231114)
                await bot_dev.send(f"ERROR finding {NAME} role because of this error\n{e}")
                return
            pass
        else:
            await ctx.send(f'Please use this command in the #Roles channel')
            return
    
    
    @commands.command(hidden=True)
    @commands.has_permissions()
    async def custom_color(self, ctx, Red, Green, Blue):
        if not CUSTOM_COLORS_ALLOWED:
            return
        global GUILD
        GUILD = ctx.guild
        #print(GUILD)
        if str(ctx.channel) == 'roles':
            c = Color(rgb=(float(Red), float(Green), float(Blue)))
            print(c)
            print(GUILD.roles)
            try:
                role = discord.utils.get(GUILD.roles, name=c)
                if role == None:
                    error = "Role = None"
                else:
                    pass
                print(f"{role} role found")
            except error:
                print("role can not be found")
                await GUILD.create_role(name=c, colour=col.from_rgb(float(Red), float(Green), float(Blue)))
                print("Role created")
            try:
                user = ctx.author
                print(user)
                await user.add_roles(role)
                print("Role added to user")
            except Exception as e:
                await ctx.send(f"ERROR creating this role. Bot devs have been informed.")
                bot_dev = ctx.guild.get_member(515364565245231114)
                await bot_dev.send(f"ERROR creating {c} role because of this error\n{e}")
                return
            await ctx.send(f'Roles has been setup.')
        else:
            return

    # USE REACTIONS TO GIVE ROLES (GET MESSAGE ID OF MY SENT ROLES MESSAGE). REFER TO Basic.py on_reaction_add() #


def setup(client):
    client.add_cog(Roles(client))
