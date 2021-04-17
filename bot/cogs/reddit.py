import discord
from discord.ext.commands import command, Cog
from asyncpraw import Reddit
from dotenv import load_dotenv
import os


client_id = os.getenv("REDDIT_APP_ID")
client_secret = os.getenv("REDDIT_APP_SECRET")
reddit = Reddit(client_id=client_id, client_secret=client_secret,
                user_agent="discord:com.example.CloverBot:1.0 (by u/RedditUser762005)")


class Reddit(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="meme", pass_context=True, help="Take a random meme from reddit")
    async def meme(self, ctx):
        subreddit = await reddit.subreddit("memes+dankmemes+wholesomememes")
        submission = await subreddit.random()
        url = submission.url
        rEmbed = discord.Embed(
            title=submission.title, description=submission.selftext, colour=discord.Colour.green())
        if url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
            rEmbed.set_image(url=url)
        rEmbed.set_author(name=submission.author)
        rEmbed.set_footer(
            text=f"{submission.score} ⬆️│{submission.num_comments} 💬")
        await ctx.send(embed=rEmbed)

    @command(name="randompost", pass_context=True, help="Obtain a random post from a random subreddit")
    async def randompost(self, ctx, subreddit=None):
        if subreddit is None:
            return await ctx.send("Please send a subreddit to obtain a post from")
        subreddit = await reddit.subreddit(str(subreddit))
        submission = await subreddit.random()
        url = submission.url
        rEmbed = discord.Embed(
            title=submission.title, description=submission.selftext, colour=discord.Colour.green())
        if url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
            rEmbed.set_image(url=url)
        rEmbed.set_author(name=str(submission.author))
        await ctx.send(embed=rEmbed)


def setup(bot):
    bot.add_cog(Reddit(bot))
