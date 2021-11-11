import discord
from discord.ext import commands
import asyncio

global USERS, timeout
USERS = [{'id': str(), "repeats": 0}]
timeout = 30


class Spam(commands.Cog):
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
                for user in USERS:
                    if str(message.author.id) == user['id']:
                        student = {'id': str(message.author.id), "repeats": int(user['repeats'])+1}
                        repeated = True
                    else:
                        student = {'id': str(message.author.id), "repeats": 1}
                        repeated = False
                USERS.append(student)
                if repeated == True:
                    if int(student['repeats']) >= 3:
                        await message.guild.ban(message.author, reason="spam")
                        await asyncio.sleep(86400)
                        await message.guild.unban(message.author)
                        return
                    if int(student['repeats']) > 1:
                        timeout = 30 * int(student['repeats'])
                    role = message.guild.get_role(907857638740619265)
                    await message.author.add_roles(role)
                    await message.author.send(f"You have been muted for {timeout} seconds due to spamming a channel.")
                    await asyncio.sleep(timeout)
                    timeout = 30
                    await message.author.remove_roles(role)
                    await message.author.send(f"You have been un-muted.")
                    repeated = False
                else:
                    if int(student['repeats']) >= 3:
                        await message.guild.ban(message.author, reason="spam")
                        await asyncio.sleep(86400)
                        await message.guild.unban(message.author)
                        return
                    timeout = 30
                    role = message.guild.get_role(907857638740619265)
                    await message.author.add_roles(role)
                    await message.author.send(f"You have been muted for {timeout} seconds due to spamming a channel.")
                    await asyncio.sleep(timeout)
                    await message.author.remove_roles(role)
                    await message.author.send(f"You have been un-muted.")
    
    @commands.Cog.listener()
    async def on_ready(self):
        global USERS
        i = 0
        while True:
            await asyncio.sleep(10)
            with open("spam_detect.txt", "r+") as f:
                f.truncate(0)
                f.close()
            i += 1
            if i == 9:
                USERS = [{'id': str(), "repeats": 0}]
                i = 0
            else:
                pass
            #print("Cleared")
    '''
    @commands.command()
    async def example(self, ctx):
        await ctx.send(f'Example: idk')
    '''
    
def setup(client):
    client.add_cog(Spam(client))
