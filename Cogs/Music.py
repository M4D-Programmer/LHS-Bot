import discord
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient
import youtube_dl, asyncio, os
from random import choice
import json


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

players = {}

current_song = 0
loop_ = False

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
    
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        #print(".")
        loop = loop or asyncio.get_event_loop()
        #print(":")
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        #print("..")
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        #print("...")
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        #print("....")
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('queues.json', 'r') as f:
            queues_file = json.load(f)
        queues_file[str(guild.id)] = {'queues': []}
        with open('queues.json', 'w') as f:
            json.dump(queues_file, f, indent=4)
        
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('queues.json', 'r') as f:
            queues_file = json.load(f)
        queues_file.pop(str(guild.id))
        with open('queues.json', 'w') as f:
            json.dump(queues_file, f, indent=4)
    
    @commands.Cog.listener()
    async def refresh_queues(self, ctx):
        with open('queues.json', 'r') as f:
            queues_file = json.load(f)
            f.close()
        queues = queues_file[str(ctx.guild.id)]['queues']
        return queues
    
    @commands.command()
    async def play(self, ctx, url : str):
        with open('queues.json', 'r') as f:
            queues_file = json.load(f)
            f.close()
        
        #global queues
        global current_song
        global loop_
        #print(".")
        server = ctx.message.guild
        queues = queues_file[str(server.id)]['queues']
        voice_channel = server.voice_client
        #voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        # , after=lambda: check_queues(self, server.id)
        #print("..")
        
        if not url:
            if queues_file[server.id]['queues'] == []:
                await ctx.send('Please provide a url or add a song to the queue.')
                pass
            else:
                if not ctx.message.author.voice:
                    await ctx.send('Please join a voice channel to use this command.')
                else:
                    voiceChannel = ctx.message.author.voice.channel
                try:
                    await voiceChannel.connect()
                    voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
                except:
                    voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
                    pass
                #print("...")
                #print(queues_file[server.id]['queues'])
                
                with open('queues.json', 'r') as f:
                    queues_file = json.load(f)
                queues_file[str(ctx.message.guild.id)]['queues'] = [url]
                with open('queues.json', 'w') as f:
                    json.dump(queues_file, f, indent=4)

                async with ctx.typing():
                    player = await YTDLSource.from_url(queues[current_song])
                    voice.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                await ctx.send(f"Now playing: **{player.title}**")
                #del(queue[0])
                pass
            #print("not url")
        else:
            if not ctx.message.author.voice:
                await ctx.send('Please join a voice channel to use this command.')
            else:
                voiceChannel = ctx.message.author.voice.channel
            try:
                await voiceChannel.connect()
                voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            except:
                voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
                pass
            #print("url")
            with open('queues.json', 'r') as f:
                queues_file = json.load(f)
            queues_file[str(ctx.message.guild.id)]['queues'] = [url]
            with open('queues.json', 'w') as f:
                json.dump(queues_file, f, indent=4)
            #print(queues_file[str(ctx.message.guild.id)]['queues'])
            #print(".....")
            async with ctx.typing():            # queues[server.id][url]
                player = await YTDLSource.from_url(url)  # , loop=client.loop
                #print("player")
                voice.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
                #print("voice")
                
                if loop_:
                    queues_file[str(ctx.message.guild.id)]['queues'].append(queues[0])
                #del(queues[0])
                
                await ctx.send(f"Now playing: **{player.title}**")
        
    '''
            try:
                for file in os.listdir("./"):
                    if file.endswith(".webm"):
                        os.remove(file)
            except PermissionError:
                await ctx.send('Please wait for the song to end or use the !stop command.')
                return
            '''


    
    """
    @commands.command()
    async def join(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if not voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send(f'I am already in a voice channel.')
    """
    
    @commands.command(help="Loops the queue and not a specific song.(Not yet ready)")
    async def loop_q(self, ctx):
        global loop_
        if loop_:
            await ctx.send(f"Stopped looping the queue.")
            loop_ = False
        else:
            await ctx.send(f"Looping the queue.")
            loop_ = True
        pass
    
    @commands.command()
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send(f'I am not in a voice channel.')
    
    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send(f'I am already paused.')
    
    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send(f'The audio is not paused.')
    
    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
    
    '''
    def check_queues(self, ID):
        if queues[ID] != []:
            player = queues[ID].pop(0)
            players[ID] = player
            player.start()
    '''
    
    @commands.command(name='queue', help='This command adds a song to the queue')
    async def queue_(self, ctx, url):
        #global queues
        
        server = ctx.message.guild.id
        voice_client = self.client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url)
        
        with open('queues.json', 'r') as f:
            queues_file = json.load(f)
        queues = queues_file[str(server)]['queues']
        
        if server in queues:
            queues[server].append(player)
        else:
            queues[server] = [player]
        
        await ctx.send(f'`{player}` added to queue!')
    
    @commands.command(help='This command removes a song from the queue', description="Ex: !remove 2\nremoves the 2nd queued song")
    async def remove(self, ctx, number):
        #global queues

        server = ctx.message.guild.id
        
        with open('queues.json', 'r') as f:
            queues_file = json.load(f)
        queues = queues_file[str(server)]['queues']
        
        try:
            del(queues[int(number)-1])
            await ctx.send(f'Your queue is now `{queues}!`')
        except:
            await ctx.send('Your queue is either **empty** or the index is **out of range**')
            
    @commands.command(help='This command shows the queue')
    async def view_q(self, ctx):
        server = ctx.message.guild.id

        with open('queues.json', 'r') as f:
            queues_file = json.load(f)
        queues = queues_file[str(server)]['queues']
        
        await ctx.send(f'Here is your queue\n`{queues}`')
    
def setup(client):
    client.add_cog(Music(client))
