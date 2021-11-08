import discord
from discord.ext import commands


WORDS = ["FUCK", "SHIT", "BITCH", "ASS", "DICK", "CUNT", "PENIS", "ASSHOLE", "DOUCHBAG", "FAGGOT", "PUSSY", "MOTHERFUCKER", "NIGGER", "NIGGA", "DAMN", "FAG"]


class Censor(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, message: str):
        if message.author.id == 694589350733807666 or message.channel.id == 893551950455521301:
            return
        CURSING = False
        CURSE_WORDS = []
        msg = ""
        for word in WORDS:
            if word.lower() in str(message.content).lower():
                CURSING = True
                CURSE_WORDS.append(word)
                #print(0)
                #msg = str(message.content).lower().replace(word.lower(), '...')
            '''
            t = 0
            for letter in word:
                print(1)
                if letter.lower() in str(message.content).lower()[t:len(word)]:
                    print(2)
                    CURSING = True
                    CURSE_WORDS.append(word)
                else:
                    return
                t += 1
            '''
        for word in CURSE_WORDS:
            msg = str(message.content).lower().replace(word.lower(), '...')
        if CURSING == True:
            if len(message.content) >= 30:
                await message.delete()
                await message.author.send(f"Please refrain from using those words.\nHere is your message `{msg}`")
            else:
                await message.delete()
                await message.author.send(f"Please refrain from using those words.")
            CURSING = False
            CURSE_WORDS = []
        pass
    '''
    @commands.command()
    async def example(self, ctx):
        await ctx.send(f'Example: idk')
    '''

def setup(client):
    client.add_cog(Censor(client))
