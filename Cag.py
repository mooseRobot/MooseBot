from discord.ext import commands
import praw, discord

reddit = praw.Reddit(
client_id="",
client_secret="",
password="",
user_agent="",
username="",
)

###### Global Grab Functions ######
async def cag_grab(subr = "", lim=0):
    global gallery_url
    global title
    gallery_url  = ""
    title = ""
    hot_posts = reddit.subreddit(subr).hot(limit = lim)
    for post in hot_posts:
        gallery_url = post.url
        title = post.title
    
    global gallery
    gallery = []
    
    try:
        """
        Attempts to grab gallery url if top post is a gallery
        """
        submission = reddit.submission(url = gallery_url)
        image_dict = submission.media_metadata
        for image_item in image_dict.values():
            largest_image = image_item['s']
            image_url = largest_image['u']
            gallery.append(image_url)
    except:
        return gallery_url

async def post_type(subreddit) -> str:
    global upvotes, post_url, redditor, body, title, text_post

    upvotes = 0
    post_url = ""
    redditor = None
    body = ""
    title = ""

    text_post = False

    hot_posts = reddit.subreddit(subreddit).hot(limit = 1)
    for post in hot_posts:
        if post.is_self:
            redditor = post.author # redditor.name
            upvotes = post.score
            post_url = post.url
            body = post.selftext 
            title = post.title
            text_post = True
        else:
            await cag_grab(subr = subreddit, lim=1)

class Cag(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Grabs top hot post from r/kpics
    @commands.command()
    async def cag(self, ctx):
        await ctx.channel.send("Grabbing image <:masaka:706682412943540244>", delete_after=2)
        # Calls global function cag_grab with parameter
        await cag_grab(subr = "kpics", lim=1)
        await ctx.channel.send(title)
        if len(gallery) > 0:
            for url in gallery:
                await ctx.channel.send(url)
        else:
            await ctx.channel.send(gallery_url)

    # Grabs top hot post from r/kpopfap
    @commands.command()
    async def cagf(self, ctx):
        await ctx.channel.send("Grabbing image <:masaka:706682412943540244>", delete_after=2)
        await cag_grab(subr = "kpopfap", lim=3)
        await ctx.channel.send(title)
        if len(gallery) > 0:
            for url in gallery:
                await ctx.channel.send(url)
        else:
            await ctx.channel.send(gallery_url)

    # Grabs top hot post from subreddit
    @commands.command()
    async def trending(self, ctx):
        async with ctx.typing():
            subreddit = str(ctx.message.content[10:])
            await post_type(subreddit)
            text = text_post
            if text == True:
                    MyEmbed = discord.Embed(title=f"{title}", url=f"{post_url}", color=0xbd0000)
                    MyEmbed.set_author(name=f"r/{subreddit}")
                    MyEmbed.add_field(name = f"{upvotes} upvotes", value = f"{body}")
                    await ctx.send(embed=MyEmbed)
                    text = False
            else:
                await ctx.channel.send(title)
                if len(gallery) > 0:
                    for url in gallery:
                        await ctx.channel.send(url)
                else:
                    await ctx.channel.send(gallery_url)

def setup(bot):
    bot.add_cog(Cag(bot))
