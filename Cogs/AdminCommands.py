import discord
from datetime import datetime
from typing import Optional
from discord.ext import commands, tasks
import os
import json


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    '''
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')
        pass
    '''

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.client.latency * 1000)}ms')
        pass

    @commands.command(name="userinfo", aliases=["ui", "memberinfo"])
    @commands.has_permissions(administrator=True)
    async def user_info(self, ctx, target: Optional[commands.MemberConverter]):
        target = target or ctx.author
        
        embed = discord.Embed(
            title="User Information",
            colour=target.colour,
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=target.avatar_url)
        
        fields = [("Name", str(target), True), 
                  ("ID", target.id, True),
                  ("Bot?", target.bot, True),
                  ("Top role", target.top_role.mention, True),
                  ("Status", str(target.status).title(), True),
                  ("Activity", f"""{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}""", True),
                  ("Created on", target.created_at.strftime("%m/%d/%Y %H:%M:%S"), True),
                  ("Joined at", target.joined_at.strftime("%m/%d/%Y %H:%M:%S"), True),
                  ("Server boosted", bool(target.premium_since), True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        
        
        await ctx.send(embed=embed)
    
    @commands.command(name="serverinfo", aliases=["si", "guildinfo"])
    @commands.has_permissions()
    async def server_info(self, ctx):
        embed = discord.Embed(
            title="Server Information",
            colour=discord.Colour.blue(),
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=ctx.guild.icon_url)
        
        fields = [("ID", ctx.guild.id, False),
                    ("Owner", str(ctx.guild.owner), True),
                    ("Region", ctx.guild.region, True),
                    ("Created on", ctx.guild.created_at.strftime("%m/%d/%Y %H:%M:%S"), True),
                    ("Members", len(ctx.guild.members), True),
                    ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                    ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                    ("Text channels", len(ctx.guild.text_channels), True),
                    ("Voice channels", len(ctx.guild.voice_channels), True),
                    ("Banned members", len(await ctx.guild.bans()), True),
                    ("Categories", len(ctx.guild.categories), True),
                    ("Roles", len(ctx.guild.roles), True),
                    ("Invites", len(await ctx.guild.invites()), True)]
        
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)


    @commands.command(description="Clears an amount of messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, _prefix):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = _prefix
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send(f"Prefix was changed to {_prefix}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f"{member.mention} has been kicked")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f"{member.mention} has been banned")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discrim = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discrim):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} has been unbanned")
                return
            return
        pass

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, *, question):
        channel = ctx.guild.get_channel(893890596895346808)
        message = await channel.send(f'{question}')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, *, member: commands.MemberConverter):
        #print("Getting roles")
        roles_list = discord.utils.get(ctx.guild.roles)
        #print(roles_list)
        muted_role = discord.utils.get(ctx.guild.role, name='Muted')
        #print("muting")
        await member.add_roles(muted_role)

        await ctx.send(f"{member.mention} has been muted")
        pass

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify an amount of messages to delete.\nExample: !clear 10')
        pass


def setup(client):
    client.add_cog(AdminCommands(client))
