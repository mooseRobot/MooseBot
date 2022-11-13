import discord, random
from discord.ext import commands

from discord.ext.commands import CommandNotFound

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=".", intents= intents, help_command = None)

def is_me(ctx): # Checks if user is me
    return ctx.author.id == id

########### Help ###########

@bot.command(alias = ['about'])
async def help(ctx):
    """
    Help command
    """
    MyEmbed = discord.Embed(title="MooseBot Help Commands", url="https://github.com/mooseRobot/MooseBot", description="Call these help menus for more commands", color=0xbd0000)
    MyEmbed.set_author(name="Created by mooseRobot", url="https://github.com/mooseRobot", icon_url="https://avatars.githubusercontent.com/u/111679444?s=400&u=e780fac96614dd28ef409f0a6e4f35f234fba5d4&v=4")
    MyEmbed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/837198834593431573/1039890752563589190/IMG_17012018_223941_0.png")
    MyEmbed.add_field(name = ".help_music", value = "Help menu for music commands")
    MyEmbed.add_field(name = ".help_reddit", value = "Help menu for available commands for reddit")
    MyEmbed.add_field(name = ".help_leveling", value = "Help menu for leveling and coins")
    MyEmbed.add_field(name = ".help_shop", value = "Shop menu for available commands to purchase WIP")
    MyEmbed.add_field(name = ".help_games", value = "Available games to play to bet coins WIP")
    MyEmbed.add_field(name = ".coinflip", value = "Flips a coin")
    await ctx.send(embed = MyEmbed)

##################################################################
############################ Events ############################

@bot.event 
async def on_ready(): # When bot is ready
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='out for .help'))
    print("Bot ready!")

@bot.event
async def on_member_join(member):
    """
    Welcome user when they join a server
    """
    guild = member.guild 
    guildname = guild.name
    # dmchannel = await member.create_dm() # creaing a dmchannel to dm a message. Needs await since its an async func
    # await dmchannel.send(f"Welcome to {guildname}") # Welcomes member
    print(f"{member.name} has joined {guildname}")
    general = discord.utils.get(member.guild.channels, name="general").id
    await bot.get_channel(general).send(f"Welcome {member.mention} to {guildname}!")
    await bot.get_channel(general).send("https://cdn.discordapp.com/attachments/837198834593431573/1039890752563589190/IMG_17012018_223941_0.png")


##################################################################
############################ Commands ############################

# ping command
@bot.command()
async def ping(ctx):
    """
    Ping command

    Used for testing purposes
    """
    await ctx.send("Pong!")

# Coinflip Command
@bot.command()
async def coinflip(ctx):
    """ Flips a coin

    Args:
        ctx (class): Represents the context in which a command is being invoked from
    """
    num = random.randint(1,2)
    if num == 1: 
        await ctx.send("Heads!")
    if num == 2:
        await ctx.send("Tails!")  

# Kicking someone out of a vc
@bot.command()
async def voicekick(ctx, user : discord.Member):
    """Kicks user from voice channel

    Args:
        user (discord.Member): User to kick from voice
    """
    guild = ctx.author.guild # Sets guild to ctx guild
    voicestate = ctx.author.voice
    uservc = user.voice
 
    if voicestate is None:
        # Checks if user is in a voice channel
        await ctx.channel.send("You must be in a voice channel to use this command!")
    elif uservc is None:
        await ctx.channel.send("User is not connected to a voice channel...")
    elif ctx.author.voice.channel.name != user.voice.channel.name:
        await ctx.channel.send("You must be in the same voice channel to use this command!")

    elif ctx.author.voice.channel.name == user.voice.channel.name:
        if ctx.author.roles[-1] >= guild.roles[-3]: # specific sets if ctx role is higher than KKK (nsfw) role then can execute command
            await user.edit(voice_channel = None)
            await ctx.channel.send(f"Kicked {user.mention}!")
        else:
            await ctx.channel.send(f"{ctx.author.mention} does not have permission to use this command.")

@voicekick.error
async def errorhandler(ctx, error):
    """ Voicekick command error handling

        Checks if error had a missing argument or if user exists in guild
    """
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to specify a member.")
    if isinstance(error, commands.errors.MemberNotFound): # Checks if error mathes error type
        await ctx.channel.send("I could not find that user...")

@bot.command()
async def kick(ctx, user : discord.Member, *, reason = None):
    """Kicks a user from server

    Args:
        user (discord.Member): User to kick from voice
        reason (str): Reason for kicking"""
    if ctx.author.roles[-1] >= ctx.author.guild[-3]: # specific sets if ctx role is higher than KKK (nsfw) role then can execute command
        await ctx.guild.kick(user, reason=None)
        await ctx.channel.send(f"Kicked {user.mention} from {user.guild}.")
    else:
        await ctx.channel.send(f"{ctx.author.mention} does not have permission to use this command.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Command not found.")


#### Main cog load/unload/reload ###
@bot.command()
@commands.check(is_me)
async def load_events(ctx):
    bot.load_extension("Events")
    await ctx.send("Events extension loaded.")

@bot.command()
@commands.check(is_me)
async def unload_events(ctx):
    bot.unload_extension("Events")
    await ctx.channel.send("Events extention Unloaded.")

@bot.command()
@commands.check(is_me)
async def reload_events(ctx):
    bot.reload_extension("Events")
    await ctx.channel.send("Events extension reloaded.")

### Music cog load/unload/reload ###
@bot.command()
@commands.check(is_me)
async def load_music(ctx):
    bot.load_extension("Music")
    await ctx.send("Music extension loaded.")

@bot.command()
@commands.check(is_me)
async def unload_music(ctx):
    bot.unload_extension("Music")
    await ctx.channel.send("Music extension Unloaded.")

@bot.command()
@commands.check(is_me)
async def reload_music(ctx):
    bot.reload_extension("Music")
    await ctx.channel.send("Music extension reloaded.")

### Cag cog load/unload/reload ###
@bot.command()
@commands.check(is_me)
async def load_cag(ctx):
    bot.load_extension("Cag")
    await ctx.channel.send("Cag extension loaded")

@bot.command()
@commands.check(is_me)
async def unload_cag(ctx):
    bot.unload_extension("Cag")
    await ctx.channel.send("Cag extension unloaded")

@bot.command()
@commands.check(is_me)
async def reload_cag(ctx):
    bot.reload_extension("Cag")
    await ctx.channel.send("Cag extension reloaded")

### Leveling cog load/unload/reload ###
@bot.command()
@commands.check(is_me)
async def load_level(ctx):
    bot.load_extension("Levels")
    await ctx.channel.send("Levels extension loaded")

@bot.command()
@commands.check(is_me)
async def unload_level(ctx):
    bot.unload_extension("Levels")
    await ctx.channel.send("Levels extension unloaded")

@bot.command()
@commands.check(is_me)
async def reload_level(ctx):
    bot.reload_extension("Levels")
    await ctx.channel.send("Levels extension reloaded")
    
bot.load_extension('Cag')
bot.load_extension("Events")
bot.load_extension("Music")
bot.load_extension("Levels")
bot.run('bot_token')
