from discord.ext import commands
from random import uniform
import json, discord

async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 0
        users[f'{user.id}']['coins'] = 0

async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp

async def level_up(users, user, message):
    secret formula
    if secret:
        await message.channel.send(f':sparkles: {user.mention} gained 50 coins and leveled up to level {lvl_end}!')
        users[f'{user.id}']['level'] = secret
        users[f'{user.id}']['coins'] += 50

def is_me(ctx):
    return ctx.author.id == 

# Leaderboard
leaderboard = {}

class Levels(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help_leveling(self, ctx):
        embed=discord.Embed(title="Leveling Basics", description="Experience is gained on sending messages or using bot commands (2x). Total xp for the next level is exponential. Leveling up grants you 50 coins", color = 0x00FFFF)
        embed.set_author(name=".help_leveling")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1036894149443588108/1041085145530241024/71985_1.gif")
        embed.add_field(name=".level @member", value="Sends member's current level", inline=False)
        embed.add_field(name=".next_level @member", value="Amount of xp needed to level up", inline=True)
        embed.add_field(name=".level_xp", value="Amount of xp required to level up at a given level.", inline=True)
        embed.add_field(name=".current_xp @member", value="Current amount of xp", inline=True)
        embed.add_field(name=".balance @member", value="Amount of coins the user has", inline=True)
        embed.add_field(name=".richest_users", value="Sends top 5 richest users", inline=True)
        embed.add_field(name=".high_lvl_users", value="Sends top 5 highest leveled users", inline=True)
        embed.add_field(name=".circulation", value="Amount of coins in circulation", inline=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('users.json', 'r') as f:
            users = json.load(f)
        await update_data(users, member)
        with open('users.json', 'w') as f:
            json.dump(users, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False:
            with open('users.json', 'r') as f:
                users = json.load(f)
            experience = 0
            if:
              Secret forumala to stopping people from farming xp

            await update_data(users, message.author)
            await add_experience(users, message.author, experience)
            await level_up(users, message.author, message)

            with open('users.json', 'w') as f:
                json.dump(users, f)

        # await self.bot.process_commands(message)

    # Returns users level
    @commands.command()
    async def level(self, ctx, member : discord.Member):
        if ctx.author == member:
            id = ctx.message.author.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            await ctx.send(f'You are at level {lvl}!')
        else:
            id = member.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(id)]['level']
            await ctx.send(f'{member.name} is at level {lvl}!')

    @level.error
    async def errorhandler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You have to specify a member.")
        if isinstance(error, commands.errors.MemberNotFound): # Checks if error mathes error type
            await ctx.channel.send("I could not find that user...")

    # Returns user's balance
    @commands.command()
    async def balance(self, ctx, member : discord.Member):
        if ctx.author == member:
            id = ctx.message.author.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[str(id)]['coins']
            await ctx.send(f'You have {coins} coins!')
        else:
            id = member.id
            with open('users.json', 'r') as f:
                users = json.load(f)
            coins = users[str(id)]['coins']
            await ctx.send(f'{member.name} has {coins} coins!')

    @balance.error
    async def errorhandler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You have to specify a member.")
        if isinstance(error, commands.errors.MemberNotFound): # Checks if error mathes error type
            await ctx.channel.send("I could not find that user...")

    # Returns amount of xp needed to level up
    @commands.command()
    async def next_level(self, ctx, member : discord.Member):

        with open('users.json', 'r') as f:
            users = json.load(f)
        experience = users[f'{member.id}']['experience']
        lvl_start = users[f'{member.id}']['level']
        next_level = (lvl_start + 1) Secret fomula
        diff =  next_level- experience
        if ctx.author == member:
            await ctx.send(f"You are {int(diff)} xp away from level {lvl_start + 1}")
        else:
            await ctx.send(f"{member.name} is {int(diff)} xp away from level {lvl_start + 1}")

    @next_level.error
    async def errorhandler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You have to specify a member.")
        if isinstance(error, commands.errors.MemberNotFound): # Checks if error mathes error type
            await ctx.channel.send("I could not find that user...")

    # Check current xp
    @commands.command()
    async def current_xp(self, ctx, member : discord.Member):
        with open('users.json', 'r') as f:
            users = json.load(f)
        experience = users[f'{member.id}']['experience']
        lvl_start = users[f'{member.id}']['level']
        level_xp = (lvl_start) secret formula
        diff =  experience - level_xp
        if ctx.author == member:
            await ctx.send(f"You have {int(diff)} xp.")
        else:
            await ctx.send(f"{member.name} has {int(diff)} xp.")

    @current_xp.error
    async def errorhandler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You have to specify a member.")
        if isinstance(error, commands.errors.MemberNotFound): # Checks if error mathes error type
            await ctx.channel.send("I could not find that user...")

    # XP needed to level up
    @commands.command()
    async def level_xp(self, ctx, num):
        level_total_xp = int(num)
        prev_total_xp = (int(num) - 1) secret formula
        diff = level_total_xp - prev_total_xp
        await ctx.send(f"Level {num} requires {int(diff)} xp to level up")

    @level_xp.error
    async def errorhandler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You have to specify a level.")

    # Coin Leaderboard
    @commands.command()
    async def richest_users(self, ctx):
        with open('users.json', 'r') as f:
            data = json.load(f)
        # Reset leaderboard
        leaderboard = {}
        for i in data.keys():
            leaderboard[i] = data[i]['coins']
        sorted_board = {k: v for k, v in sorted(leaderboard.items(), key=lambda item: item[1])}
        first, fcoins = int(list(sorted_board.keys())[-1]), int(list(sorted_board.values())[-1])
        second, scoins = int(list(sorted_board.keys())[-2]), int(list(sorted_board.values())[-2])
        third, tcoins = int(list(sorted_board.keys())[-3]), int(list(sorted_board.values())[-3])
        fourth, focoins = int(list(sorted_board.keys())[-4]), int(list(sorted_board.values())[-4])
        fifth, ficoins = int(list(sorted_board.keys())[-5]), int(list(sorted_board.values())[-5])

        embed=discord.Embed(title="Top 5 Richest Users!", color = 0x00FFFF)
        embed.set_thumbnail(url=f"{self.bot.get_user(first).avatar_url}")
        embed.add_field(name=f"1. {self.bot.get_user(first).name}", value=f"{fcoins} coins", inline=False)
        embed.add_field(name=f"2. {self.bot.get_user(second).name}", value=f"{scoins} coins", inline=False)
        embed.add_field(name=f"3. {self.bot.get_user(third).name}", value=f"{tcoins} coins", inline=False)
        embed.add_field(name=f"4. {self.bot.get_user(fourth).name}", value=f"{focoins} coins", inline=False)
        embed.add_field(name=f"5. {self.bot.get_user(fifth).name}", value=f"{ficoins} coins", inline=False)
        await ctx.send(embed=embed)

    # Levels Leaderboard
    @commands.command()
    async def high_lvl_users(self, ctx):
        with open('users.json', 'r') as f:
            data = json.load(f)
        # Reset leaderboard
        leaderboard = {}
        for i in data.keys():
            leaderboard[i] = data[i]['level']
        sorted_board = {k: v for k, v in sorted(leaderboard.items(), key=lambda item: item[1])}
        first, flevel = int(list(sorted_board.keys())[-1]), int(list(sorted_board.values())[-1])
        second, slevel = int(list(sorted_board.keys())[-2]), int(list(sorted_board.values())[-2])
        third, tlevel = int(list(sorted_board.keys())[-3]), int(list(sorted_board.values())[-3])
        fourth, folevel = int(list(sorted_board.keys())[-4]), int(list(sorted_board.values())[-4])
        fifth, filevel = int(list(sorted_board.keys())[-5]), int(list(sorted_board.values())[-5])

        embed=discord.Embed(title="Top 5 Highiest Level Users!", color = 0x00FFFF)
        embed.set_thumbnail(url=f"{self.bot.get_user(first).avatar_url}")
        embed.add_field(name=f"1. {self.bot.get_user(first).name}", value=f"Level {flevel}", inline=False)
        embed.add_field(name=f"2. {self.bot.get_user(second).name}", value=f"Level {slevel} ", inline=False)
        embed.add_field(name=f"3. {self.bot.get_user(third).name}", value=f"Level {tlevel} ", inline=False)
        embed.add_field(name=f"4. {self.bot.get_user(fourth).name}", value=f"Level {folevel} ", inline=False)
        embed.add_field(name=f"5. {self.bot.get_user(fifth).name}", value=f"Level {filevel} ", inline=False)
        await ctx.send(embed=embed)

    # Checks amount of coins in circulation
    @commands.command()
    async def circulation(self, ctx):
        with open('users.json', 'r') as f:
            data = json.load(f)
        
        total = 0
        for i in data.keys():
            total += data[i]['coins']

        await ctx.send(f'There are {total} coins in circulation.')

    # Adds coins
    @commands.command()
    @commands.check(is_me)
    async def add_coins(self, ctx, n,member : discord.Member):
        with open('users.json', 'r') as f:
            users = json.load(f)

        users[f'{member.id}']['coins'] += int(n)
        await ctx.send(f"Our glorious leader {ctx.author.mention} has bestowed upon you {n} coins!")
        with open('users.json', 'w') as f:
            json.dump(users, f)

    @add_coins.error
    async def errorhandler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Master, you must specify a member!")
        if isinstance(error, commands.errors.MemberNotFound): # Checks if error mathes error type
            await ctx.channel.send("栄光ある団長、申し訳ございませんでした。メンバーがお探ししませんでした！")

    # Removes n amount of coins
    @commands.command()
    @commands.check(is_me)
    async def remove_coins(self, ctx, n,member : discord.Member):
        with open('users.json', 'r') as f:
            users = json.load(f)

        users[f'{member.id}']['coins'] -= int(n)
        await ctx.send(f"You a roach for real! Scram!")
        with open('users.json', 'w') as f:
            json.dump(users, f)

    @remove_coins.error
    async def errorhandler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Master, you must specify a member!")
        if isinstance(error, commands.errors.MemberNotFound): # Checks if error mathes error type
            await ctx.channel.send("栄光ある団長、申し訳ございませんでした。メンバーがお探ししませんでした！")


def setup(bot):
    bot.add_cog(Levels(bot))
