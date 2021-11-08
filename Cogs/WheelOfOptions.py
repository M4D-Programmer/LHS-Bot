import discord
from discord.ext import commands
import random, json


options = []
class WheelOfOptions(commands.Cog):
    def __init__(self, client):
        self.client = client
    '''
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is online')
        pass
    '''
    @commands.command()
    async def add_option(self, ctx, *, option):
        options.append(option)
        await ctx.send(f'Option added.')
    
    @commands.command(help="Saves a preset as a name. Ex: !save_preset name. (only one can be saved for now)")
    async def save_preset(self, ctx, *,name):
        with open('WheelPresets.json', 'r') as f:
            WheelPresets = json.load(f)

        WheelPresets[str(ctx.guild.id)]['preset'] = f"{name}"
        WheelPresets[str(ctx.guild.id)]['options'] = options
        
        with open('WheelPresets.json', 'w') as f:
            json.dump(WheelPresets, f, indent=4)
        
        await ctx.send(f'Preset saved as {name}')
    
    @commands.command()
    async def show_presets(self, ctx):
        with open('WheelPresets.json', 'r') as f:
            WheelPresets = json.load(f)
        await ctx.send(f"""`{WheelPresets[str(ctx.guild.id)]['preset']}, {WheelPresets[str(ctx.guild.id)]['options']}`""")
    
    @commands.command(help="Ex: !delete_preset name.")
    async def delete_preset(self, ctx, *,name):
        with open('WheelPresets.json', 'r') as f:
            WheelPresets = json.load(f)
        
        WheelPresets[str(ctx.guild.id)]['preset'] = f""
        WheelPresets[str(ctx.guild.id)]['options'] = f""
        
        with open('WheelPresets.json', 'w') as f:
            json.dump(WheelPresets, f, indent=4)
        
        await ctx.send(f"Preset `{name}` has been deleted.")
    
    @commands.command(help="Ex: !delete_option OptionName.")
    async def delete_option(self, ctx, *, option : str):
        if option in options:
            options.remove(option)
        else:
            pass
        await ctx.send(f'Option deleted.')
    
    @commands.command()
    async def show_options(self, ctx):
        await ctx.send(f"""{str(options).replace("'", '')}""")
        
    @commands.command(help="Erases the options.")
    async def clear_options(self, ctx):
        await ctx.send(f"""Options were cleared.""")
        
    @commands.command()
    async def spin_preset(self, ctx):
        print(".")
        print("..")
        with open('WheelPresets.json', 'r') as f:
            WheelPresets = json.load(f)

        json_server_id = WheelPresets[str(ctx.guild.id)]

        list_from_json = json_server_id['options']
        
        chosen_option = random.choice(list_from_json)
        
        print(chosen_option)
        await ctx.send(f"""The wheel landed on {chosen_option}.""")

    @commands.command(help="Spins the wheel.")
    async def spin(self, ctx):
        if options == []:
            await ctx.send(f"Please add options for this command to work.")
        else:
            shuffles = random.randint(0, 20)
            for x in range(shuffles):
                random.shuffle(options)
                chosen_option = random.choice(options)
            await ctx.send(f"""The wheel landed on {chosen_option}.""")
        pass

def setup(client):
    client.add_cog(WheelOfOptions(client))
