from discord.ext import commands
import praw

class myCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    # Only Jamal
    @commands.Cog.listener()
    async def on_message(self, msg):
        if 'jamal' in msg.content.lower():
            await msg.channel.send("https://cdn.discordapp.com/attachments/938930303811084328/1039878947032281098/channels4_profile.jpg")    

    # Bet
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return
        else:
            if 'bet' in msg.content.lower():
                await msg.channel.send('OH BET!')
                for i in range(2):
                    await msg.channel.send('BET!')
                await msg.channel.send("https://cdn.discordapp.com/attachments/939096040274034758/1040595616784465960/IMG_4065.jpg")    

def setup(bot):
    bot.add_cog(myCog(bot))