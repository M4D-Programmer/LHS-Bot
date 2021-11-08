import discord
from discord.ext import commands
import random, asyncio


class CoinFlip(commands.Cog):
    def __init__(self, client):
        self.client = client
    '''
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')
        pass
    '''
    @commands.command()
    async def flip(self, ctx):
        coinsides = ['Heads', 'Tails']
        await ctx.send(f'The coin landed on...:drum:')
        random.shuffle(coinsides)
        random.shuffle(coinsides)
        random.shuffle(coinsides)
        CoinSide = random.choice(coinsides)
        await asyncio.sleep(2)
        await ctx.send(f'{CoinSide}')


def setup(client):
    client.add_cog(CoinFlip(client))
