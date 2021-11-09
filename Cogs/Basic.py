import discord
from discord.ext import commands, tasks
import os
import json
#from datetime import datetime
import datetime
global approved
approved = False
# z̯̯͡a̧͎̺l̡͓̫g̹̲o̡̼̘
global NickRules
NickRules = [
    "**Rule 1:** No blank or \"invisible\" names\n",
    "**Rule 2:** No slurs or other offensive sentiments\n",
    "**Rule 3:** No noisy unicode characters - for example, **z̯̯͡a̧͎̺l̡͓̫g̹̲o̡̼̘ ** or byte order marks\n",
    "**Rule 4:** No nicknames designed to annoy other users"]

global Rules
Rules = [
    "**Rule 1:** Be respectful to everyone. This means DO NOT make racist remarks, or send rude comments that may make people uncomfortable. We're all high schoolers here so let's act like it\n",
    "**Rule 2:** No NSFW in general channels! Some people can get uncomfortable with NSFW. If you want to see/post any NSFW content, you can in the NSFW channel\n",
    "**Rule 3:** Don't spam or purposely annoy anyone. Refrain from spamming bots, @ everyone, @ admin, and @ bot-dev @ moderator tags. Only use them if there is an issue or a bug\n",
    "**Rule 4:** Keep discussions relevant to channel topics and guidelines. If you need help, please ask for it in a help channel. Not in general chats\n",
    "**Rule 5:** Do not provide or request answers on projects/graded coursework/exams. If you are helping someone, please help them the best you can without giving away the answer\n",
    "**Rule 6:** Do not impersonate or argue with staff\n",
    "**Rule 7:** Nothing against Discords Terms of Service (TOS) (https://discord.com/terms)\n",
    "**Rule 8:** Nothing against Discords Community Guidelines (https://discord.com/guidelines)\n",
    "**Rule 9:** Just have common sense on what is and isn't allowed\n",
    "\n**Failing to comply to these rules can result in a temporary or permanant mute/ban!**"]

class Basic(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        pass

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def nickrules(self, ctx):
        #print("Send nick rules")
        msg = ""
        #print("created msg var")
        try:
            for x in NickRules:
                #print("in loop")
                msg += str(x) + "\n"
                #print("added")
            
            #print(msg)
            embed = discord.Embed(
                title=f"**Nickname policy**",
                description=f"In order to keep things pleasant and workable for all members, we enforce the following requirements regarding your nickname. Developers reserve the right to change the nickname of any user for any reason. Failure to comply with these requirements may result in you losing the right to change your nickname. We also reserve the right to discipline users with offensive usernames, regardless of the nickname they're using.\n\n{msg}",
                color=discord.Color.blue()
            )
            await ctx.channel.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.has_permissions(administrator=True)
    @commands.command(hidden=True, help="Sends a specific nickname rule.")
    async def nickrule(self, ctx, num: int):
        embed = discord.Embed(
            title=f"Rule {num}",
            description=f"""{str(NickRules[num-1]).replace(f"**Rule {num}:**", "")}""",
            color=discord.Color.blue()
        )
        await ctx.channel.send(embed=embed)

    
    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def rules(self, ctx):
        msg = ""
        for x in Rules:
            msg += str(x) + "\n"

        embed = discord.Embed(
            title=f"**Rules**",
            description=f"{msg}",
            color=discord.Color.blue()
        )
        await ctx.channel.send(embed=embed)

    @commands.command(help="Sends a specific rule.")
    async def rule(self, ctx, num: int):
        embed = discord.Embed(
            title=f"Rule {num}",
            description=f"""{str(Rules[num-1]).replace(f"**Rule {num}:**", "")}""",
            color=discord.Color.blue()
        )
        await ctx.channel.send(embed=embed)

    @commands.command(help="Sends a picture of the yearly calendar.")
    @commands.has_permissions(administrator=True)
    async def calendar(self, ctx):
        _time_ = datetime.datetime.now()
        month = _time_.strftime("%b")
        day = _time_.strftime("%d")
        
        embed = discord.Embed(
            title=f"Weekly Calendar for {month}"
        )

        fields = [(f"{int(day)}", f"Something", True),
                  (f"{int(day)+1 if int(day) <= 29 else None}", f"Something", True),
                  (f"{int(day)+2 if int(day) <= 29 else None}", f"Something", True),
                  (f"{int(day)+3 if int(day) <= 29 else None}", f"Something", True),
                  (f"{int(day)+4 if int(day) <= 29 else None}", f"Something", True),
                  (f"{int(day)+5 if int(day) <= 29 else None}", f"Something", True),
                  (f"{int(day)+6 if int(day) <= 29 else None}", f"Something", True),
                  (f"{int(day)+7 if int(day) <= 29 else None}", f"Something", True),
                  (f"LINK:", f"https://www.lancaster.k12.oh.us/Calendar/1#m=9&s=1&t=1:2:24:38&y=2021", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        #embed.set_footer(text="https://www.lancaster.k12.oh.us/Calendar/1#m=9&s=1&t=1:2:24:38&y=2021", icon_url="https://www.lancaster.k12.oh.us/images/userfiles/1625/my%20files/user_image_c18_icon.ico")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, help="Sends your suggestion to admins for approval, then to the suggestions channel (if approved).")
    async def suggest(self, ctx, *, msg: str):
        await ctx.channel.purge(limit=1)
        #print("purge")
        channel = ctx.guild.get_channel(832380306605604874)
        #print("send")
        message = await channel.send(f"""{ctx.author.mention} wants to make this suggestion: "{msg}" """)
        reactions = ['✅', '❌']
        for emoji in reactions:
            await message.add_reaction(emoji)
        #print(ctx.author)
        adminRole = ctx.guild.get_role(831294127487844352)
        #print(adminRole)
        
            #return user == ctx.guild.owner and str(reaction.emoji) == '✅'
        #print("test")
        #cache_msg = discord.utils.get(client.messages, id=message.id)
        #for reactor in message.reactions:
        #    print("print")
        #    print(reactor)
        #    reactors = await client.get_reaction_users(reactor)
        #print("test over")
        #print("wait")
        reaction, user = await self.client.wait_for('reaction_add', check=self.on_reaction_add)
        if approved == True:
            print("Approved")
        else:
            pass
        #print("after")
        
        #client.on_reaction_add('✅', client.guild.owner)
        pass

def setup(client):
    client.add_cog(Basic(client))
