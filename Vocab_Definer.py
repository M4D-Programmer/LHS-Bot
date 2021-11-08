import discord
from discord.ext import commands
from PyDictionary import PyDictionary



class VocabDefine(commands.Cog):
    def __init__(self, client):
        self.client = client
    '''
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')
        pass
    '''

    
    @commands.command(help="Defines a single or multiple words.")
    async def define(self, ctx, *, words_to_define:str):
        words = []
        if "," in words_to_define:
            try:
                words = words_to_define.split(", ")
            except:
                words = words_to_define.split(",")
        else:
            words.append(words_to_define)
        async with ctx.typing():
            for word in words:
                dictionary = PyDictionary(word)
                meaning = dictionary.meaning(word)
                #print(f"meaning: {meaning}")
                #syns = dictionary.synonym(word)
                #syns = dictionary.getSynonyms()
                #print(f"syns: {syns}")
                #ants = dictionary.antonym(word)
                #ants = dictionary.getAntonyms()
                #print(f"ants: {ants}")
                print("embed")
                embed = discord.Embed(
                    title=f"{str(word)} definition:",
                    description=str(meaning).replace("{", '').replace(
                        "}", '').replace("[", '').replace("]", '').replace("'", ''),
                    color=discord.Color.blue()
                )
                #define_embed.set_thumbnail(url=)
                #print("field 1")
                #embed.add_field(name="Synonyms", value=str(syns).replace(
                #    "{", '').replace("}", '').replace("[", '').replace("]", '').replace("'", ''), inline=True)
                #print("field 2")
                #embed.add_field(name="Antonyms", value=str(ants).replace(
                #    "{", '').replace("}", '').replace("[", '').replace("]", '').replace("'", ''), inline=True)
                #dictionary.meaning(str(word))
                await ctx.send(embed=embed)

    @commands.command(hidden=True, help="Defines words for a specific subject. Gives an image, synonyms, and antonyms")
    async def defs(self, ctx, subject, *words: list):
        for word in words:
            pass
    '''
    @commands.command()
    async def antonym(self, ctx, word):
        #dictionary.antonym(str(word))

        await ctx.send(f'https://www.thesaurus.com/browse/{word}')
    '''
    @commands.command(help="Provides a link to the word being used in a sentence.")
    async def WordInSent(self, ctx, word):
        await ctx.send(f'https://wordsinasentence.com/{word}-in-a-sentence/')

def setup(client):
    client.add_cog(VocabDefine(client))
