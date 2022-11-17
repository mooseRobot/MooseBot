import discord, time, youtube_dl, random, asyncio
from discord.ext import commands

queue = []

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'extract_flat': True,
    'skip_download': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'force-ipv4': True,
    'cachedir': False
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class music(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.vc_connected = False

    #Help menu
    @commands.command()
    async def help_music(self,ctx):
        embed=discord.Embed(title="Music Commands", description="Available music commands", color = 0x00FFFF)
        embed.set_author(name=".help_leveling")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1036894455715868723/1041228686113898546/unknown.png")
        embed.add_field(name = ".p {yt url}", value = "Plays youtube song")
        embed.add_field(name = ".stop", value = "Stop/skips current song")
        embed.add_field(name = ".pause", value = "Pauses current song")
        embed.add_field(name = ".resume", value = "Resume song")
        embed.add_field(name = ".queue", value = "Shows queue")
        embed.add_field(name = ".join", value = "Joins the vc")
        embed.add_field(name = ".disconnect", value = "Disconnects from vc")
        embed.add_field(name = ".sigma", value = "Sigma circlejerk")
        embed.add_field(name = ".voicekick", value = "Starts a vote kick a user from a voice channel")
        await ctx.send(embed=embed)

    # Join user's current voice channel
    @commands.command()
    async def join(self, ctx):
        userChannel = ctx.author.voice
        voice = ctx.channel.guild.voice_client

        # Connects bot if its not in a voice channel
        if self.vc_connected == False and userChannel is not None:
            await userChannel.channel.connect() # Join VC
            voice = ctx.channel.guild.voice_client
            self.vc_connected = True
        
        # Moves to user's current voice channel
        elif userChannel is not None:
            await ctx.voice_client.move_to(userChannel.channel)
        
        # Checks if user is not connected to a voice channe;
        elif userChannel is None:
            await ctx.send("You must be in a voice channel to use this command!")
        
        # Disconnects from inactivity
        await asyncio.sleep(90)
        await voice.disconnect()
        if self.vc_connected = True:
            await ctx.send("Disconnected due to inactivity.")
            self.vc_connected = False

    
    # Test vc_connected attribute
    @commands.command()
    async def vc_state(self, ctx):
        await ctx.channel.send("pass")
        print(self.vc_connected)
        await ctx.send(self.vc_connected)

        time.sleep(1)
        await ctx.author.voice.channel.connect()
        self.vc_connected = True
        print(self.vc_connected)
        await ctx.send(str(self.vc_connected))

        time.sleep(1)
        await ctx.voice_client.disconnect()
        self.vc_connected = False
        print(str(self.vc_connected))
        await ctx.send((str(self.vc_connected)))


    @commands.command(aliases=['plays', 'p'])
    async def play(self, ctx, url):

        # Checks if user/bot is in a voice channel
        userChannel = ctx.author.voice
        voice = ctx.channel.guild.voice_client

        # Connects bot if its not in a voice channel
        if self.vc_connected == False and userChannel is not None:
            await userChannel.channel.connect() # Join VC
            voice = ctx.channel.guild.voice_client
            self.vc_connected = True
        
        # Moves to user's current voice channel
        elif userChannel is not None:
            await ctx.voice_client.move_to(userChannel.channel)
        
        # Checks if user is not connected to a voice channe;
        elif userChannel is None:
            await ctx.send("You must be in a voice channel to use this command!")

        # Appends requested song to queue
        if "&" in url:
            url = url[:url.index('&')]
        queue.append(url)

        if not voice.is_playing():
            async with ctx.typing():
                player = await YTDLSource.from_url(queue[0], loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after = lambda e : asyncio.run_coroutine_threadsafe(play_next(ctx), self.bot.loop))
                embed = discord.Embed(title="Now playing", description=f"[{player.title}]({player.url}) [{ctx.author.mention}]")
                await ctx.send(embed=embed)
                queue.pop(0) # removes song from queue
        else:
            await ctx.send("Added to Queue")

        async def play_next(ctx):
            # Plays next song
            if len(queue) > 0:
                player = await YTDLSource.from_url(queue[0], loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), self.bot.loop))
                embed = discord.Embed(title="Now playing", description=f"[{player.title}]({player.url}) [{ctx.author.mention}]")
                await ctx.send(embed=embed)
                queue.pop(0)
            else:
                await asyncio.sleep(90) #wait 1 minute and 30 seconds
                if not voice.is_playing():
                    await voice.disconnect()
                    if self.vc_connected = True:
                        await ctx.send("Disconnected due to inactivity.")
                        self.vc_connected = False

    #Stop, Resume and Pause
    @commands.command()
    async def pause(self, ctx):
        voice = ctx.channel.guild.voice_client
        if voice.is_playing() == True:
            voice.pause()
            await ctx.send("Paused")
        else:
            await ctx.send("Bot is not playing Audio!")

    @commands.command(aliases = ["skip"])
    async def stop(self, ctx):
        voice = ctx.channel.guild.voice_client
        if voice.is_playing() == True:
            voice.stop()
            await ctx.send("Skipped!")
        else:
            await ctx.send("Bot is not playing Audio!")

    @commands.command()
    async def resume(self, ctx):
        voice = ctx.channel.guild.voice_client
        if voice.is_playing() == True:
            await ctx.send("Bot is playing Audio!")
        else:
            voice.resume()


    # Sends queue
    @commands.command()
    async def queue(self, ctx):
        if len(queue) == 0:
            await ctx.send("No songs in queue.")
        elif len(queue) == 1:
            await ctx.send(f"Up next {str(queue[0])}")
        elif len(queue) == 2:
            await ctx.send(f"Up next: {str(queue[0])} and {len(queue) - 1} song after that.")
        else:
            await ctx.send(f"Up next: {str(queue[0])} and {len(queue) - 1} songs after that.")

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect() # Disconnects
        self.vc_connected = False

    # Sigma circlejerk
    @commands.command()
    async def sigma(self, ctx):
        channel = ctx.author.voice
        if channel is None:
            await ctx.channel.send(random.choice(["What is it... What is it?", "Barrier unsucsessful!", "My barrier has been overwhelmed!", "Hold it together, hold it together...!", "I... I need to think!", "It's wrong... It's all wrong!", "Mass, velocity... no, no, no!"]))
        else:
            await ctx.channel.send("HET UNIVERSUM ZINGT VOOR MIJ!!")
            ydl_opts = {'format': 'bestaudio'} # plays best possible audio
            with youtube_dl.YoutubeDL(ydl_opts) as ydl: # initialize yt-dl
                info = ydl.extract_info("https://www.youtube.com/watch?v=YOYqhs-LJrU", download=False) # Get a dictionary named info containing all video info
                URL = info['formats'][0]['url'] # Grabs url which leads to audio file
            time.sleep(0.8)
            await ctx.author.voice.channel.connect() # Connects to vc
            self.vc_connected = True # Connected
            voice = ctx.channel.guild.voice_client # initializes new audio player
            voice.play(discord.FFmpegPCMAudio(URL)) # Plays sigma audio
            time.sleep(7)
            await ctx.voice_client.disconnect() # Disconnects
            self.vc_connected = False # Disconnect

def setup(bot):
    bot.add_cog(music(bot))
