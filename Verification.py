import discord
import datetime
from typing import Optional
from discord.ext import commands, tasks
import os
import json
from bot import GUILD_ID
import asyncio
global OPEN_DATE_ACTIVE
from bot import OPEN_DATE_ACTIVE, DATE


class Verification(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(893050749930598410)
        #GUILD = self.client.get_guild(831170627901587466)
        #role2 = GUILD.get_role(894285516843937823)  # HIDDEN ROLE #           ### FIND A WAY TO HAVE NEW MEMBERS VERIFY BEFORE SEEING SERVER ###
        #await member.add_roles(role2)
        await channel.send(f"Ex: !verify first_name last_name school_email")
        pass
    '''
    @commands.Cog.listener()
    async def on_message(self, message: str):
        pass
    '''
    @commands.command(help="type \"!verify [first_name] [last_name] [email]\" without [] and with your name and email.")
    async def verify(self, ctx, FNAME, LNAME, EMAIL):
        if ctx.channel.id != 893050749930598410:
            return
        else:
            if int(EMAIL[0:2]) == 22:
                GRADE = "Senior"
            elif int(EMAIL[0:2]) == 23:
                GRADE = "Junior"
            elif int(EMAIL[0:2]) == 24:
                GRADE = "Sophomore"
            elif int(EMAIL[0:2]) == 25:
                GRADE = "Freshman"
            
            with open('Users.json', 'r') as f:
                Users = json.load(f)
                #print(Users)
            for user in Users:
                if Users[user]['email'] == EMAIL and int(user) != ctx.author.id:
                    EMAIL_IS_USED = True
                    print("EMAIL USED")
                    SAME_USER = False
                    print("NOT SAME USER")
                    break
                else:
                    EMAIL_IS_USED = False
                    pass
                '''
                elif int(user) == ctx.author.id and Users[user]['email'] != EMAIL:
                    EMAIL_IS_USED = False
                    break
                if int(user) == ctx.author.id:
                    SAME_USER = True
                    print("SAME USER")
                    break
                else:
                    SAME_USER = False
                '''
            _time_ = datetime.datetime.now()
            year = _time_.strftime("%Y")
            
            if FNAME[:2].lower() not in EMAIL and LNAME[0:4].lower() not in EMAIL and "@lcsschools.net" not in EMAIL:
                print("Not a school email!")
                await ctx.send(f'Sorry, but the info you gave me is incorrect. Please enter all of the information accurately.\nIf you think this is a mistake, please contact @bot-dev')
                return
            elif int(EMAIL[0:2]) <= (int(year[2:]) - 1) or int(EMAIL[0:2]) >= (int(year[2:]) + 5):
                print("Not an active student!")
                await ctx.send(f'Sorry! You are not an active student in LHS.\nIf you think this is a mistake, please contact <@&831329030602752020>')
                return
            elif EMAIL_IS_USED == True and SAME_USER == False:
                await ctx.send(f'Sorry! That email was already used for another account.')
            else:
                print("Active student!")
                with open('Users.json', 'r') as f:
                    Users = json.load(f)
                    Users[str(ctx.author.id)] = {'username': "", 'name': '', 'email': '', 'grade': ''}
                    Users[str(ctx.author.id)]['username'] = f"{ctx.author.name}"
                    Users[str(ctx.author.id)]['name'] = f"{FNAME.capitalize()} {LNAME.capitalize()}"
                    Users[str(ctx.author.id)]['email'] = f"{EMAIL}"
                    Users[str(ctx.author.id)]['grade'] = f"{GRADE}"
                with open('Users.json', 'w') as f:
                    json.dump(Users, f, indent=4)
                await ctx.send(f'Thank you! Have fun in the server!')
                GUILD = ctx.guild
                role = GUILD.get_role(889967435288051755)  # REGISTERED ROLE #
                user = ctx.author
                #print(user)
                SENIOR = 2022
                JUNIOR = 2023
                SOPHOMORE = 2024
                FRESHMAN = 2025
                
                await user.edit(nick=f"{FNAME.capitalize()} {LNAME[0].capitalize()}")
                
                if role in user.roles:
                    await user.remove_roles(role)
                else:
                    await user.add_roles(role)
                
                role = discord.utils.get(GUILD.roles, name=f"{GRADE}")
                if role in user.roles:
                    await user.remove_roles(role)
                else:
                    await user.add_roles(role)
                
                if OPEN_DATE_ACTIVE == True:
                    GUILD = ctx.guild
                    role2 = GUILD.get_role(894285516843937823)  # HIDDEN ROLE #
                    #await member.remove_roles(role1)
                    await user.add_roles(role2)
                else:
                    pass
                await ctx.channel.purge(limit=100)
        pass


# get school email from user #


# email code #


# get code from user #


# add user to Users.json with email #


# give user Registered Role #


def setup(client):
    client.add_cog(Verification(client))
