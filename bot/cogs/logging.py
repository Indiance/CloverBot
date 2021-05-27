from discord import Embed, Colour
from discord.ext.commands import Cog


class Logging(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message_edit(self, before, after):
        em = Embed(title=":pencil2: Messaged Edited",
                   description=f"A message was edited in {before.channel.mention}",
                   colour=Colour.orange())
        em.add_field(name="Message author",
                     value=f"{before.author.mention}", inline=False)
        em.add_field(name="Previous content of the message",
                     value=f"{before.content}", inline=False)
        em.add_field(name="New content of the message",
                     value=f"{after.content}", inline=False)
        channel = self.bot.get_channel(787528401279385631)
        await channel.send(embed=em)

    @Cog.listener()
    async def on_message_delete(self, message):
        em = Embed(title=":wastebasket: Message deleted",
                   description=f"A message was deleted in {message.channel.mention}",
                   colour=Colour.red())
        em.add_field(name="Message author",
                     value=f"{message.author.mention}", inline=False)
        em.add_field(name="Content in the message", value=f"{message.content}")
        channel = self.bot.get_channel(787528401279385631)
        await channel.send(embed=em)

    @Cog.listener()
    async def on_member_ban(self, guild, user):
        async for entry in guild.audit_logs(limit=1):
            author = entry.user
        em = Embed(title="User was banned from the server",
                   description="A user was banned from the server",
                   colour=Colour.red())
        em.add_field(name="User that was banned", value=user.mention, inline=False)
        em.add_field(name="Person that did the ban", value=author.mention, inline=False)
        channel = self.bot.get_channel(787528401279385631)
        await channel.send(embed=em)

def setup(bot):
    bot.add_cog(Logging(bot))
