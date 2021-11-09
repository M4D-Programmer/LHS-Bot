import discord
from discord.ext import commands, tasks
import datetime
import time
from bot import OPEN_DATE_ACTIVE, DATE


class Open_Date(commands.Cog):
    def __init__(self, client):
        self.client = client
    '''
    @commands.Cog.listener()
    async def on_member_join(self, member):
        global OPEN_DATE_ACTIVE
        server = self.client.get_guild(831170627901587466)
        if OPEN_DATE_ACTIVE == True:
            role = discord.utils.get(server.roles, name=f"{DATE}")
            await member.add_roles(role)
        else:
            pass
    '''
    
    @tasks.loop(hours=1)
    async def check_date(self):
        global OPEN_DATE_ACTIVE
        if OPEN_DATE_ACTIVE == True:
            date = datetime.datetime.now().date()
            #print(date)
            #print(DATE)
            if str(date) == DATE:
                server = self.client.get_guild(831170627901587466)
                role = discord.utils.get(server.roles, name=f"{DATE}")
                for member in server.members:
                    await member.remove_roles(role)
                # GET HIDDEN ROLE AND REMOVE FROM ALL USERS #
                await role.edit(name=f"Hidden")
                OPEN_DATE_ACTIVE = False
                # FIND A WAY TO SAVE WHO IS/ISNT REGISTERED OR CHANGE REGISTERED PERMS #
                pass
            else:
                pass
        else:
            pass
    
    @commands.command()
    async def Lockdown(self, ctx, date):
        server = self.client.get_guild(831170627901587466)
        global OPEN_DATE_ACTIVE
        global DATE
        if OPEN_DATE_ACTIVE == True:
            OPEN_DATE_ACTIVE = False
            role = server.get_role(889967435288051755) # REGISTERED ROLE #
            #permissions = discord.Permissions()
            #permissions.update(view_channel=True)
            #await role.edit(permissions=permissions)
            print(False)
            for cat in server.categories:
                #category = discord.utils.get(server.categories, name=x)
                await cat.set_permissions(role, view_channel=True)
            for role in server.roles:
                if role.name == 'Opens {DATE}':
                    await role.edit(name=f"Hidden")
                    break
            return
        else:
            OPEN_DATE_ACTIVE = True
            print("True")
        DATE = date
        # UPDATE ROLE NAME TO TIME TILL OPEN #
        todays_date = datetime.datetime.now().date()
        #time_left = int(DATE[7:]) - int((todays_date[7:]))
        #print(time_left)
        
        role = server.get_role(889967435288051755)  # REGISTERED ROLE #
        #permissions = discord.Permissions()
        #permissions.update(view_channel=False)
        #await role.edit(permissions=permissions)
        
        for cat in server.categories:
            #category = discord.utils.get(server.categories, name=x)
            await cat.set_permissions(role, view_channel=False)
        
        for role in server.roles:
            if role.name == 'Hidden':
                await role.edit(name=f"Opens {DATE}")
                break
        
        for member in server.members:
            if member.id == 694589350733807666 or member.id == 368105370532577280 or member.id == 675531542910730242:
                pass
            else:
                GUILD = ctx.guild
                #role1 = discord.utils.get(GUILD.roles, name="Registered")
                role2 = server.get_role(894285516843937823)  # HIDDEN ROLE #
                #await member.remove_roles(role1)
                await member.add_roles(role2)
                
        # UPDATE HIDDEN ROLE NAME TO TIME TILL OPEN #
        
        # POST MESSAGE IN SERVER-CLOSED CHANNEL #
        
        channel = server.get_channel(895132489612394507)
        await channel.send(f"The Server Will Open On {DATE}")


def setup(client):
    client.add_cog(Open_Date(client))
