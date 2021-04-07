# discord Imports
import discord
from discord import Embed, Member, File
from discord.ext.commands import command, Cog, group, is_owner
#other imports
from random import choice
from dotenv import load_dotenv
<<<<<<< HEAD
import aiohttp
import io
=======
from aiohttp import ClientSession
from io import BytesIO
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c

load_dotenv()


class Miscellaneous(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

<<<<<<< HEAD
    @commands.command(name='8ball', pass_context=True)
=======
    @command(name='8ball', pass_context=True)
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
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

<<<<<<< HEAD
    @commands.command(name='shutdown', pass_context=True, help="Shutdown the bot")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.bot.logout()

    @commands.command(name='wasted', pass_context=True)
    async def wasted(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        wastedsession = aiohttp.ClientSession()
=======
    @command(name='shutdown', pass_context=True, help="Shutdown the bot")
    @is_owner()
    async def shutdown(self, ctx):
        await ctx.bot.logout()

    @command(name='wasted', pass_context=True)
    async def wasted(self, ctx, member: Member = None):
        if not member:
            member = ctx.author

        wastedsession = ClientSession()
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
        async with wastedsession.get(f"https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to obtain image")
                await wastedsession.close()
            else:
<<<<<<< HEAD
                data = io.BytesIO(await img.read())
                await ctx.send(file=discord.File(data, 'wasted.png'))
                await wastedsession.close()

    @commands.command(name="invert", pass_context=True)
    async def invert(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        invertsession = aiohttp.ClientSession()
=======
                data = BytesIO(await img.read())
                await ctx.send(file=File(data, 'wasted.png'))
                await wastedsession.close()

    @command(name="invert", pass_context=True)
    async def invert(self, ctx, member: Member = None):
        if not member:
            member = ctx.author

        invertsession = ClientSession()
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
        async with invertsession.get(f"https://some-random-api.ml/canvas/invert?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to obtain image")
                await invertsession.close()
            else:
<<<<<<< HEAD
                data = io.BytesIO(await img.read())
                await ctx.send(file=discord.File(data, 'inverted.png'))
                await invertsession.close()

    @commands.command(name="pixelate", pass_context=True)
    async def pixelate(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        invertsession = aiohttp.ClientSession()
=======
                data = BytesIO(await img.read())
                await ctx.send(file=File(data, 'inverted.png'))
                await invertsession.close()

    @command(name="pixelate", pass_context=True)
    async def pixelate(self, ctx, member: Member = None):
        if not member:
            member = ctx.author

        invertsession = ClientSession()
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
        async with invertsession.get(f"https://some-random-api.ml/canvas/pixelate?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to obtain image")
                await invertsession.close()
            else:
<<<<<<< HEAD
                data = io.BytesIO(await img.read())
                await ctx.send(file=discord.File(data, 'pixelated.png'))
                await invertsession.close()

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        hEmbed = discord.Embed(title="Help",
                               description="Use the +help (command) to learn more about a specif command. anything in angular brackets <> is mandatory and anything in [] is optional",
                               colour=ctx.author.color)
=======
                data = BytesIO(await img.read())
                await ctx.send(file=File(data, 'pixelated.png'))
                await invertsession.close()

    @group(invoke_without_command=True)
    async def help(self, ctx):
        hEmbed = Embed(title="Help",
                       description="Use the +help (command) to learn more about a specif command. anything in angular brackets <> is mandatory and anything in [] is optional",
                       colour=ctx.author.color)
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
        hEmbed.add_field(name=":hammer: Moderation",
                         value="kick, ban, unban, warn, clearwarns, warnings",
                         inline=False)
        hEmbed.add_field(name=":game_die: Miscellaneous",
                         value="8ball, wasted, invert, pixelate",
                         inline=False)
        hEmbed.add_field(name=":desktop: Reddit",
                         value="meme, randompost",
                         inline=False)
        hEmbed.add_field(name=":newspaper: News",
                         value="countrynews, topicnews",
                         inline=False)
        hEmbed.add_field(name=":headphones: Music",
                         value="connect, disconnect, play, queue",
                         inline=False)
        await ctx.send(embed=hEmbed)

    @help.command()
    async def kick(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(title="Kick",
                            description="kick a member from the server",
                            color=ctx.author.color)
=======
        em = Embed(title="Kick",
                   description="kick a member from the server",
                   color=ctx.author.color)
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
        em.add_field(name="**Syntax**", value="+kick <member> [reason]")
        await ctx.send(embed=em)

    @help.command()
    async def ban(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(title="Ban",
                            description="Ban a member from the server",
                            color=ctx.author.color)
=======
        em = Embed(title="Ban",
                   description="Ban a member from the server",
                   color=ctx.author.color)
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
        em.add_field(name="**Syntax**", value="+ban <member> [reason]")
        await ctx.send(embed=em)

    @help.command()
    async def unban(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(title="Unban",
                            description="Unban a member from the server",
                            color=ctx.author.color)
        em.add_field(name="**Syntax**",
                      value="+unban <member>#<discriminator>")
=======
        em = Embed(title="Unban",
                   description="Unban a member from the server",
                   color=ctx.author.color)
        em.add_field(name="**Syntax**",
                     value="+unban <member>#<discriminator>")
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
        await ctx.send(embed=em)

    @help.command()
    async def warn(self, ctx):
<<<<<<< HEAD
        wEm = discord.Embed(title="Warn",
                            description="Unban a member from the server",
                            color=ctx.author.color)
=======
        wEm = Embed(title="Warn",
                    description="Unban a member from the server",
                    color=ctx.author.color)
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
        wEm.add_field(name="**Syntax**", value="+warn <member> [reason]")
        await ctx.send(embed=wEm)

    @help.command()
    async def warnings(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(title="Warnings",
                             description="Show the warnings that a member has",
                             color=ctx.author.color)
=======
        em = Embed(title="Warnings",
                   description="Show the warnings that a member has",
                   color=ctx.author.color)
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
        em.add_field(name="**Syntax**", value="+warnings <member>")
        await ctx.send(embed=em)

    @help.command()
    async def clearwarns(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(title="Clearwarns",
                             description="Clear the warnings that a user has",
                             color=ctx.author.color)
=======
        em = Embed(title="Clearwarns",
                   description="Clear the warnings that a user has",
                   color=ctx.author.color)
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
        em.add_field(name="**Syntax**", value="+clearwarns <member>")
        await ctx.send(embed=em)

    @help.command(name="8ball")
    async def _8ball(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(title="8ball",
                           description="Answer your questions using the 8ball.",
                           color=ctx.author.color)
=======
        em = Embed(title="8ball",
                   description="Answer your questions using the 8ball.",
                   color=ctx.author.color)
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
        em.add_field(name="**Syntax**", value="+8ball <question>")
        await ctx.send(embed=em)

    @help.command(name="invert")
    async def help_invert(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(
=======
        em = Embed(
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
            title="Invert", description="Invert a person's avatar", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+invert [member]")
        await ctx.send(embed=em)

    @help.command(name="Pixelate")
    async def help_wasted(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(
=======
        em = Embed(
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
            title="Pixelate", description="Pixelate someone's profile picture", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+pixelate [member]")
        await ctx.send(embed=em)

    @help.command(name="meme")
    async def reddit_meme(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(
=======
        em = Embed(
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
            title="Meme", description="Take a random meme from reddit", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+meme")
        await ctx.send(embed=em)

    @help.command(name="randompost")
    async def reddit_randompost(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(
=======
        em = Embed(
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
            title="random post", description="obtain a random post from reddit given a subreddit name", color=ctx.author.color)
        em.add_field(name="**syntax**", value="+randompost <subreddit>")
        await ctx.send(embed=em)

    @help.command()
    async def countrynews(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(
=======
        em = Embed(
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
            title="Countrynews", description="Pick some news from a country. The country name should be two letters", color=ctx.author.color)
        em.add_field(name="**syntax**",
                     value="+countrynews <country> <number of articles>")
        await ctx.send(embed=em)

    @help.command()
    async def topicnews(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(
=======
        em = Embed(
>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c
            name="Topic news", description="Get some news from various sources given a topic", color=ctx.author.color)
        em.add_field(name="**Syntax**",
                     value="+topicnews <topic> <number of articles>")
        await ctx.send(embed=em)

    @help.command()
    async def connect(self, ctx):
<<<<<<< HEAD
        em = discord.Embed(
            title="Connect", description="Join a voice channel", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+connect [voice channel name]")
        await ctx.send(embed=em)
    
    @help.command()
    async def play(self, ctx):
        em = discord.Embed(title="Play", description="Play a song", color=ctx.author.color)
        em.add_field(name="**Syntax**",value="+play <song name> or +play <url>")
        await ctx.send(embed=em)
    
    async def queue(self, ctx):
        em = discord.Embed(title="Queue", description="Show the queue in a song", color=ctx.author.color)
        em.add_field(name="**Syntax",value="+queue")
        await ctx.send(embed=em)
=======
        em = Embed(
            title="Connect", description="Join a voice channel", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+connect [voice channel name]")
        await ctx.send(embed=em)

    @help.command()
    async def play(self, ctx):
        em = Embed(title="Play", description="Play a song",
                   color=ctx.author.color)
        em.add_field(name="**Syntax**",
                     value="+play <song name> or +play <url>")
        await ctx.send(embed=em)

    async def queue(self, ctx):
        em = Embed(
            title="Queue", description="Show the queue in a song", color=ctx.author.color)
        em.add_field(name="**Syntax", value="+queue")
        await ctx.send(embed=em)

>>>>>>> 0a31baa6c0563891def67bd366fe7f1c639b675c

def setup(bot):
    bot.add_cog(Miscellaneous(bot))