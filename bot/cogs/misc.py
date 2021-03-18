import discord
from discord.ext import commands
from random import choice
import requests
import json
from dotenv import load_dotenv
import os
from googletrans import Translator

translator = Translator()


load_dotenv()

api_key = os.getenv('NEWSAPI_KEY')


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball', pass_context=True, help="Predict something with our 8ball.")
    async def ball(self, ctx, *question):
        choices = [
            "As I see it, yes", "Ask again later", "Better not tell you now",
            "Cannot predict now", "Concentrate and ask again",
            "Don’t count on it", "It is certain", "It is decidedly so", "Most likely",
            "My reply is no", "My sources say no", " Outlook not so good",
            "Outlook good", "Reply hazy, try again", "Signs point to yes",
            "Very doubtful", "Without a doubt", "Yes", "You may rely on it"]
        answer = choice(choices)
        if ' '.join(question) == '':
            return await ctx.send("You have not asked anything. Please try again")
        else:
            await ctx.send('{}? {}'.format(' '.join(question), answer))

    @commands.command(name='version', pass_context=True, help="Get the version of this bot")
    async def versionembed(self, ctx):
        vEmbed = discord.Embed(title="Current Version",
                               description="Version 0.0.2",
                               color=0x00ff00)
        vEmbed.add_field(name="Date of Release", value="13th December 2020",
                         inline=False)
        vEmbed.add_field(name="Changes since previous version",
                         value="Warn category: warn a user, clear warns and show warns")
        vEmbed.set_footer(text="Still in development")
        vEmbed.set_author(name="Indiance#2326")
        await ctx.send(embed=vEmbed)

    @commands.command(name="topnews", pass_context=True, help="Find the top news of a country")
    async def topnews(self, ctx, country: str = None, count: int = None):
        if country is None:
            return await ctx.send("Please provide a country.")
        if count is None:
            return await ctx.send("Please provide some number of articles")
        url = f"https://newsapi.org/v2/top-headlines?country={country.lower()}&apiKey={api_key}"
        responses = requests.get(url)
        articles = json.loads(responses.text)
        i = 1
        for article in articles['articles']:
            nEmbed = discord.Embed(
                title=translator.translate(article['title']).text, description=translator.translate(article['description']).text, colour=discord.Colour.blurple())
            nEmbed.set_author(name=article['author'])
            nEmbed.set_image(url=article['urlToImage'])
            await ctx.send(embed=nEmbed)
            if i < count:
                i += 1
            else:
                break


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
