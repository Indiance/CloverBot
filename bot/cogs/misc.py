# discord Imports
from discord import Embed, Member, File, Spotify, Game
import discord
from discord.ext.commands import command, Cog, is_owner

# other imports
from random import choice
from aiohttp import ClientSession
from typing import Optional
from io import BytesIO
from datetime import datetime as dt
from pistonapi import PistonAPI

piston = PistonAPI()


class Miscellaneous(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='8ball', pass_context=True, help="Predict events or answer questions using the 8ball")
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

    @command(name='wasted', pass_context=True, help="Add the wasted image on top of a user's avatar")
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

    @command(name="invert", pass_context=True, help="Invert the colors on a user's avatar")
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

    @command(name="pixelate", pass_context=True, help="Pixelate someone's avatar")
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

    @command(name="userinfo", pass_context=True, help="Show information about a user")
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
        em.add_field(name=f"Roles [{len(mentions)}]",
                     value=f"{' '.join(mentions) if mentions else 'None'}", inline=False)
        em.add_field(name="Top Role", value=user.top_role.mention)
        em.add_field(name="Status", value=str(user.status).title())
        em.add_field(name="Activity",
                     value=f"{user.activity.name if user.activity else 'N/A'}")
        em.add_field(name="Is the user a bot?", value=user.bot)
        em.set_thumbnail(url=user.avatar_url)
        for activity in user.activities:
            if isinstance(activity, Spotify):
                em.add_field(
                    name="Activity", value=f"Listening to {activity.title} by {activity.artist}")
            elif isinstance(activity, Game):
                em.add_field(name="Activity", value=f"Playing {activity.name}")
        await ctx.send(embed=em)

    @command(name="serverinfo", pass_context=True, help="Show information about a server")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        bots = [member for member in guild.members if member.bot]
        users = [member for member in guild.members if not member.bot]
        roles = [role.mention for role in guild.roles if role.mentionable]
        em = Embed(
            title=f"Showing information about {guild.name}", color=guild.owner.color)
        em.add_field(name="Date the server was created",
                     value=guild.created_at.strftime("%d/%m/%Y %H:%M"), inline=False)
        em.add_field(name="Server owner", value=guild.owner.mention)
        em.add_field(name="Number of users", value=len(users))
        em.add_field(name="Number of bots", value=len(bots))
        em.add_field(name="Number of categories", value=len(guild.categories))
        em.add_field(name="Number of text channels",
                     value=len(guild.text_channels))
        em.add_field(name="Number of voice channels",
                     value=len(guild.voice_channels))
        em.add_field(name="Region", value=guild.region)
        em.add_field(name="Number of roles", value=len(guild.roles))
        em.add_field(name="Roles in the server",
                     value=f"{' '.join(roles) if roles else 'None'}", inline=False)
        em.set_thumbnail(url=guild.icon_url)
        em.set_footer(text=guild.id)
        await ctx.send(embed=em)

    @command(name="compile", pass_context=True, help="Run code. Done using PistonAPI")
    async def compile(self, ctx, *, code):
        lang = code.split("\n")[0].replace("```","")
        code = "\n".join(code.split("\n")[1:-1])
        print(code)
        versions = {
                "python": "3.9",
                "py": "3.9",
                "java": "15.0.2",
                "javascript":"16.3.0",
                "js": "16.3.0",
                "rust": "1.50.0",
                "gcc": "10.2.0",
                "c": "10.2.0",
                "c++": "10.2.0",
                "cpp": "10.2.0",
                "typescript": "4.2.3",
                "ts": "4.2.3",
                "lua": "5.4.2",
                "rust": "1.50.0",
                "swift": "5.3.3",
                "perl": "5.26.1",
                "scala": "3.0.0",
                "php": "8.0.2",
                "octave": "6.2.0",
                "go": "1.16.2"
            }
        if lang in versions.keys():
            output = piston.execute(language=lang, version=versions[lang], code=code)
            outputEmbed = Embed(title="Your code was compiled!", description=f"\nOutput:```{output}```", color=discord.Color.red())
            await ctx.send(embed=outputEmbed)
        else:
            await ctx.send("There was an error. Either you did not provide a language or the language does not exist")
def setup(bot):
    bot.add_cog(Miscellaneous(bot))
