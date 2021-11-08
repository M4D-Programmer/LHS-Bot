import discord
from discord.ext import commands
import random


class _8Ball(commands.Cog):
    def __init__(self, client):
        self.client = client
    '''
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')
        pass
    '''
    @commands.command(aliases=['8ball'], description="Can also use !8ball")
    async def _8ball(self, ctx, *, question):
        EightBall = ":8ball:"
        eightball_List = ["It is certain.",
                      "It is decidedly so.",
                      "Without a doubt.",
                      "Yes - definitely.",
                      "You may rely on it.",
                      "As I see it, yes.",
                      "Most likely.",
                      "Outlook good.",
                      "Yes.",
                      "Signs point to yes.",
                      "Reply hazy, try again.",
                      "Ask again later.",
                      "Better not tell you now.",
                      "Cannot predict now.",
                      "Concentrate and ask again.",
                      "Don't count on it.",
                      "My reply is no.",
                      "My sources say no.",
                      "Outlook not so good.",
                      "Very doubtful."]
        await ctx.send(f'{EightBall}**Question:** {question}\n      **Answer:** {random.choice(eightball_List)}')
        pass


def setup(client):
    client.add_cog(_8Ball(client))
