import discord
from discord.ext import commands
import json

EMAILS = []

GUILD_ID = 831170627901587466


class Bot_to_Bot(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message:str):
        if message.channel.id == 893551950455521301:
            #print("Working")
            msg = str(message.content)
            tweet = str(message.content)
            #print(tweet)
            #print(len(TO_DEL))
            await message.delete()
            #print(msg)
            #msg = msg.replace(TO_DEL, '')
            #print(msg)
            if "<@&832295240021835806>" in msg:
                if msg.startswith("a_knuckles@lcsschools.net"):
                    channel = self.client.get_channel(832300103275905124)
                    msg = msg[25:-823]
                    await channel.send(msg)
                else:
                    pass
            elif "<@&835259672385552443>" in msg:
                if msg.startswith("s_burre@lcsschools.net"):
                    channel = self.client.get_channel(836259392437092383)
                    msg = msg[22:-620]
                    await channel.send(msg)
                else:
                    pass
            elif "<@&831902709597732864>" in tweet:
                print("TWEET")
                channel = self.client.get_channel(831535497683664926)
                await channel.send(tweet)
            elif "<@&831902085141364797>" in msg:
                print("NEWS")
        else:
            return
        
    '''
    @commands.command()
    async def example(self, ctx):
        await ctx.send(f'Example: idk')
    '''


def setup(client):
    client.add_cog(Bot_to_Bot(client))
