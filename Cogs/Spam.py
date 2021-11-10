import discord
from discord.ext import commands
import asyncio

class Example(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message:str):
        counter = 0
        with open("spam_detect.txt", "r+") as f:
            for lines in f:
                if lines.strip("\n") == str(message.author.id):
                    counter += 1
            f.writelines(f"{str(message.author.id)}\n")
            if counter > 4:
                # add muted role #
                role = message.guild.get_role(907857638740619265)
                await message.author.add_roles(role)
                await message.author.send(f"You have been muted for 30 seconds due to spamming a channel.")
                await asyncio.sleep(30)
                await message.author.add_roles(role)
                await message.author.send(f"You have been un-muted.")
    
    @commands.Cog.listener()
    async def on_ready(self):
        #print('Bot is online')
        while True:
            await asyncio.sleep(10)
            with open("spam_detect.txt", "r+") as f:
                f.truncate(0)
                f.close()
            print("Cleared")
    '''
    @commands.command()
    async def example(self, ctx):
        await ctx.send(f'Example: idk')
    '''
    
def setup(client):
    client.add_cog(Example(client))
