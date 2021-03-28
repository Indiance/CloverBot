import discord
from discord.ext import commands
from random import choice
from dotenv import load_dotenv
import aiohttp
import io

load_dotenv()


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command(name='8ball', pass_context=True)
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

    @commands.command(name='shutdown', pass_context=True, help="Shutdown the bot")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.bot.logout()

    @commands.command(name='wasted', pass_context=True)
    async def wasted(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        wastedsession = aiohttp.ClientSession()
        async with wastedsession.get(f"https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to obtain image")
                await wastedsession.close()
            else:
                data = io.BytesIO(await img.read())
                await ctx.send(file=discord.File(data, 'wasted.png'))
                await wastedsession.close()

    @commands.command(name="invert", pass_context=True)
    async def invert(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        invertsession = aiohttp.ClientSession()
        async with invertsession.get(f"https://some-random-api.ml/canvas/invert?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to obtain image")
                await invertsession.close()
            else:
                data = io.BytesIO(await img.read())
                await ctx.send(file=discord.File(data, 'inverted.png'))
                await invertsession.close()

    @commands.command(name="pixelate", pass_context=True)
    async def pixelate(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        invertsession = aiohttp.ClientSession()
        async with invertsession.get(f"https://some-random-api.ml/canvas/pixelate?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to obtain image")
                await invertsession.close()
            else:
                data = io.BytesIO(await img.read())
                await ctx.send(file=discord.File(data, 'pixelated.png'))
                await invertsession.close()

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        hEmbed = discord.Embed(title="Help",
                               description="Use the +help (command) to learn more about a specif command. anything in angular brackets <> is mandatory and anything in [] is optional",
                               colour=ctx.author.color)
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
        kEm = discord.Embed(title="Kick",
                            description="kick a member from the server",
                            color=ctx.author.color)
        kEm.add_field(name="**Syntax**", value="+kick <member> [reason]")
        await ctx.send(embed=kEm)

    @help.command()
    async def ban(self, ctx):
        bEm = discord.Embed(title="Ban",
                            description="Ban a member from the server",
                            color=ctx.author.color)
        bEm.add_field(name="**Syntax**", value="+ban <member> [reason]")
        await ctx.send(embed=bEm)

    @help.command()
    async def unban(self, ctx):
        uEm = discord.Embed(title="Unban",
                            description="Unban a member from the server",
                            color=ctx.author.color)
        uEm.add_field(name="**Syntax**",value="+unban <member>#<discriminator>")
        await ctx.send(embed=uEm)
        
    @help.command()
    async def warn(self, ctx):
    	wEm = discord.Embed(title="Warn",
    	description="Unban a member from the server",
    	color=ctx.author.color)
    	wEm.add_field(name="**Syntax**", value="+warn <member> [reason]")
    	await ctx.send(embed=wEm)
    
    @help.command()
    async def warnings(self, ctx):
    	waEm = discord.Embed(title="Warnings",
    	description="Show the warnings that a member has",
    	color=ctx.author.color)
    	waEm.add_field(name="**Syntax**",value="+warnings <member>")
    
    @help.command()
    async def clearwarns(self, ctx):
    	cwEm = discord.Embed(title="Clearwarns",
    	description="Clear the warnings that a user has",
    	color=ctx.author.color)
    	cwEm.add_field(name="**Syntax**",value="+clearwarns <member>")
    
    @help.command()
    async def 8ball(self, ctx):
    	em = discord.Embed(title="8ball", 
    	description="Answer your questions using the 8ball.",
    	color=ctx.author.color)
    	em.add_field(name="**Syntax**",value="+8ball <question>")
    
    @help.command()
    async def 


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
