import discord
from discord.ext import commands
from googletrans import Translator
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('NEWSAPI_KEY')


class News(commands.Cog):
    def __init__:
        self.bot = bot

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
