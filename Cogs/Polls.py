import discord
from discord.ext import commands


class Suggestion(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        try:
            print('reaction added')
            #print(str(reaction))
            print(user)
            #print(user.roles)
            #if user == self.client:
            #    print("returned")
            #    return
            for role in user.roles:
                #print(role.name)
                if role.name == "admin" or role.name == "bot-dev":
                    print("admin detected")
                    if reaction == "\u2705" or reaction == "✅":
                        print("Approved")
                        approved = True
                        return approved
                    elif reaction == "\u274c" or reaction == "❌":
                        print("Not Approved")
                        approved = False
                        return approved
            else:
                return

            #for reactor in message.reactions:
            #    print("for loop")
            #    print(reactor)
            #    reactors = await client.get_reaction_users(reactor)
        except:
            pass
    
    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def poll(self, ctx, *, question):
        channel = ctx.guild.get_channel(832342203723939851)
        message = await channel.send(f'New Poll: {question}')
        await message.add_reaction('✅')
        await message.add_reaction('❌')


def setup(client):
    client.add_cog(Suggestion(client))
