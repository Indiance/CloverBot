from discord import Embed
from discord.ext.commands import Cog, command
from googletrans import Translator
from json import loads
from requests import get
from dotenv import load_dotenv
import os

load_dotenv()

translator = Translator()

api_key = os.getenv('NEWSAPI_KEY')


class News(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="countrynews", aliases=['cnews', 'cn'], pass_context=True, help="Find the top news of a country")
    async def cnews(self, ctx, country: str = None, count: int = None):
        if country is None:
            return await ctx.send("Please provide a country.")
        if count is None:
            return await ctx.send("Please provide some number of articles")
        url = f"https://newsapi.org/v2/top-headlines?country={country.lower()}&apiKey={api_key}"
        responses = get(url)
        articles = loads(responses.text)
        i = 1
        if articles['articles'] == []:
            return await ctx.send("There are no news articles for this country")

        for article in articles['articles']:
            nEmbed = Embed(
                title=translator.translate(article['title']).text, description=translator.translate(article['description']).text, colour=discord.Colour.blurple())
            nEmbed.set_author(name=article['author'])
            nEmbed.set_image(url=article['urlToImage'])
            await ctx.send(embed=nEmbed)
            if i < count:
                i += 1
            else:
                break

    @command(name="topicnews", aliases=['tnews', 'tn'], pass_context=True, help="Find news based on a query")
    async def tnews(self, ctx, query: str = None, count: int = None):
        if query is None:
            return await ctx.send("You haven't sent a query to search for the news on")
        if count is None:
            return await ctx.send("You haven't given a number of articles to search through")
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
        responses = get(url)
        articles = loads(responses.text)
        i = 1
        if articles['articles'] == []:
            return await ctx.send("There are no news articles for this query")

        for article in articles['articles']:
            nEmbed = Embed(
                title=translator.translate(article['title']).text, description=translator.translate(article['description']).text, colour=discord.Colour.blurple())
            nEmbed.set_author(name=article['author'])
            nEmbed.set_image(url=article['urlToImage'])
            await ctx.send(embed=nEmbed)
            if i < count:
                i += 1
            else:
                break


def setup(bot):
    bot.add_cog(News(bot))
