from discord.ext.commands import command, Cog
from discord import Member, File
from aiohttp import ClientSession
from io import BytesIO
from typing import Optional

class Canvas(Cog):
    def __init__(self, bot):
        self.bot=bot

    @command(name='wasted', pass_context=True, help="Add the wasted image on top of a user's avatar")
    async def wasted(self, ctx, member: Optional[Member]):
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
    async def invert(self, ctx, member: Optional[Member]):
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
    async def pixelate(self, ctx, member: Optional[Member]):
        if not member:
            member = ctx.author

        pixelsession = ClientSession()
        async with pixelsession.get(f"https://some-random-api.ml/canvas/pixelate?avatar={member.avatar_url_as(format='png')}") as img:
            if img.status != 200:
                await ctx.send("Unable to obtain image")
                await pixelsession.close()
            else:
                data = BytesIO(await img.read())
                await ctx.send(file=File(data, 'pixelated.png'))
                await pixelsession.close()

    @command(name="tweet", pass_context=True, help="Tweet something")
    async def tweet(self, ctx, member: Optional[Member], *tweet):
        if member is None:
            member = ctx.author
        tweetsession = ClientSession()
        async with tweetsession.get(f"https://some-random-api.ml/canvas/tweet?avatar={member.avatar_url_as(format='png')}&username={member.display_name}&displayname={member.display_name}&comment={'+'.join(tweet)}") as img:
            if img.status != 200:
                await ctx.send('unable to send the image')
                await tweetsession.close()
            else:
                data = BytesIO(await img.read())
                await tweetsession.close()
                await ctx.send(file=File(data, 'pixelated.png'))

def setup(bot):
    bot.add_cog(Canvas(bot))
