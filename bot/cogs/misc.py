# discord Imports
import discord
from discord import Embed, Member, File
from discord.ext.commands import command, Cog, group, is_owner
# other imports
from random import choice
from dotenv import load_dotenv
from aiohttp import ClientSession
from typing import Optional
from io import BytesIO
from datetime import datetime as dt

load_dotenv()


class Miscellaneous(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @command(name='8ball', pass_context=True)
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

    @command(name='shutdown', pass_context=True, help="Shutdown the bot")
    @is_owner()
    async def shutdown(self, ctx):
        await ctx.bot.close()

    @command(name='wasted', pass_context=True)
    async def wasted(self, ctx, member: Member = None):
        if not member:
            member = ctx.author

        wastedsession = ClientSession()
        async with wastedsession.get(f"https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to obtain image")
                await wastedsession.close()
            else:
                data = BytesIO(await img.read())
                await ctx.send(file=File(data, 'wasted.png'))
                await wastedsession.close()

    @command(name="invert", pass_context=True)
    async def invert(self, ctx, member: Member = None):
        if not member:
            member = ctx.author

        invertsession = ClientSession()
        async with invertsession.get(f"https://some-random-api.ml/canvas/invert?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to obtain image")
                await invertsession.close()
            else:
                data = BytesIO(await img.read())
                await ctx.send(file=File(data, 'inverted.png'))
                await invertsession.close()

    @command(name="pixelate", pass_context=True)
    async def pixelate(self, ctx, member: Member = None):
        if not member:
            member = ctx.author

        invertsession = ClientSession()
        async with invertsession.get(f"https://some-random-api.ml/canvas/pixelate?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to obtain image")
                await invertsession.close()
            else:
                data = BytesIO(await img.read())
                await ctx.send(file=File(data, 'pixelated.png'))
                await invertsession.close()

    @command(name="userinfo", pass_context=True)
    async def userinfo(self, ctx, member: Optional[Member]):
        user = member or ctx.author
        em = Embed(title=f"Showing user information for {user.name}#{user.discriminator}",
            colour=user.color,
            description=user.mention,
            timestamp=dt.utcnow())
        em.add_field(name="Created at",
                     value=user.created_at.strftime("%d/%m/%Y %H:%M"))
        em.add_field(name="Joined server at",
                     value=user.joined_at.strftime("%d/%m/%Y %H:%M"))
        mentions = [role.mention for role in user.roles if role.mentionable]
        em.add_field(name=f"Roles [{len(mentions)}]", value=f"{' '.join(mentions) if mentions else 'None'}", inline=False)
        em.add_field(name="Top Role", value=user.top_role.mention)
        em.add_field(name="Status", value=str(user.status).title())
        em.add_field(name="Activity", value=f"{user.activity.name if user.activity else 'N/A'}")
        em.add_field(name="Is the user a bot?", value=user.bot)
        em.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=em)

    @command(name="serverinfo", pass_context=True)
    async def serverinfo(self, ctx):
        guild = ctx.guild
        em = Embed(title="Showing information about the server", description=f"Server name: {guild.name}", color=guild.owner.color)
        em.add_field(name="Date the server was created", value=guild.created_at.strftime("%d/%m/%Y %H:%M"), inline=False)
        em.add_field(name="Number of members", value=guild.member_count)
        em.add_field(name="Number of roles", value=len(guild.roles))
        em.add_field(name="Number of channels", value=len(guild.channels))
        em.add_field(name="Number of text channels", value=len(guild.text_channels))
        em.add_field(name="Number of voice channels", value=len(guild.voice_channels))
        roles = [role.mention for role in guild.roles if role.mentionable]
        em.add_field(name="Roles in the server", value=f"{' '.join(roles) if roles else 'None'}")
        em.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=em)

    @group(invoke_without_command=True)
    async def help(self, ctx):
        hEmbed = Embed(title="Help",
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
        await ctx.send(embed=hEmbed)

    @help.command()
    async def kick(self, ctx):
        em = Embed(title="Kick",
                   description="kick a member from the server",
                   color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+kick <member> [reason]")
        await ctx.send(embed=em)

    @help.command()
    async def ban(self, ctx):
        em = Embed(title="Ban",
                   description="Ban a member from the server",
                   color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+ban <member> [reason]")
        await ctx.send(embed=em)

    @help.command()
    async def unban(self, ctx):
        em = Embed(title="Unban",
                   description="Unban a member from the server",
                   color=ctx.author.color)
        em.add_field(name="**Syntax**",
                     value="+unban <member>#<discriminator>")
        await ctx.send(embed=em)

    @help.command()
    async def warn(self, ctx):
        wEm = Embed(title="Warn",
                    description="Unban a member from the server",
                    color=ctx.author.color)
        wEm.add_field(name="**Syntax**", value="+warn <member> [reason]")
        await ctx.send(embed=wEm)

    @help.command()
    async def warnings(self, ctx):
        em = Embed(title="Warnings",
                   description="Show the warnings that a member has",
                   color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+warnings <member>")
        await ctx.send(embed=em)

    @help.command()
    async def clearwarns(self, ctx):
        em = Embed(title="Clearwarns",
                   description="Clear the warnings that a user has",
                   color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+clearwarns <member>")
        await ctx.send(embed=em)

    @help.command()
    async def lock(self, ctx):
        em = Embed(title="lock",
                   description="Lock a channel and sends why. It locks the channel where the command was issued unless another channel is provided",
                   color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+lock <channel> [reason]")
        await ctx.send(embed=em)

    @help.command()
    async def unlock(self, ctx):
        em = Embed(title="unlock",
                   description="Unlock a channel that has been locked. Unlocks channel where the command was issued unless another channel is provided",
                   color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+unlock <channel>")
        await ctx.send(embed=em)

    @help.command(name="8ball")
    async def _8ball(self, ctx):
        em = Embed(title="8ball",
                   description="Answer your questions using the 8ball.",
                   color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+8ball <question>")
        await ctx.send(embed=em)

    @help.command(name="invert")
    async def help_invert(self, ctx):
        em = Embed(
            title="Invert", description="Invert a person's avatar", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+invert [member]")
        await ctx.send(embed=em)

    @help.command(name="Pixelate")
    async def help_wasted(self, ctx):
        em = Embed(
            title="Pixelate", description="Pixelate someone's profile picture", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+pixelate [member]")
        await ctx.send(embed=em)

    @help.command(name="meme")
    async def reddit_meme(self, ctx):
        em = Embed(
            title="Meme", description="Take a random meme from reddit", color=ctx.author.color)
        em.add_field(name="**Syntax**", value="+meme")
        await ctx.send(embed=em)

    @help.command(name="randompost")
    async def reddit_randompost(self, ctx):
        em = Embed(
            title="random post", description="obtain a random post from reddit given a subreddit name", color=ctx.author.color)
        em.add_field(name="**syntax**", value="+randompost <subreddit>")
        await ctx.send(embed=em)

    @help.command()
    async def countrynews(self, ctx):
        em = Embed(
            title="Countrynews", description="Pick some news from a country. The country name should be two letters", color=ctx.author.color)
        em.add_field(name="**syntax**",
                     value="+countrynews <country> <number of articles>")
        await ctx.send(embed=em)

    @help.command()
    async def topicnews(self, ctx):
        em = Embed(
            name="Topic news", description="Get some news from various sources given a topic", color=ctx.author.color)
        em.add_field(name="**Syntax**",
                     value="+topicnews <topic> <number of articles>")
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
