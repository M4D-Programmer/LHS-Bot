import discord
from discord.ext import commands
import math
import requests

class Math(commands.Cog):
    def __init__(self, client):
        self.client = client
    '''
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')
        pass
    '''
    
    @commands.command(help="Get the answer to a math expression. Ex: 2 miles + 4 Km\nAnswer: 7.218688 km")
    async def expres(self, ctx, *, expression):
        url = "https://evaluate-expression.p.rapidapi.com/"
        querystring = {"expression": f"{expression}"}
        headers = {
            'x-rapidapi-key': "a88f176a3dmsh3f114520413e445p1919e6jsn1718da079774",
            'x-rapidapi-host': "evaluate-expression.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        #print(response.text)
        await ctx.send(response.text)


def setup(client):
    client.add_cog(Math(client))
