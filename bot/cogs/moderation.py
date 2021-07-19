from discord.ext.commands import Cog, command, has_permissions
from discord import Member, Embed, Game, Colour, TextChannel
import asyncio
from typing import Optional
from discord.utils import get


class Moderation(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        game = Game('+help')
        await self.bot.change_presence(activity=game)

    @Cog.listener()
    async def on_message(self, message):
        if message.guild:
            return
        if message.author == self.bot.user:
            return
        dmEmbed = Embed(title="Ticket opened",
                        description=f"Message received from {message.author.mention}", color=Colour.dark_red())
        dmEmbed.add_field(name="Content of the message", value=message.content)
        channel = self.bot.get_channel(787528401279385631)
        await channel.send(embed=dmEmbed)
        await message.channel.send("Message sent successfully")

    @command(name="send", pass_context=True, help="Send a dm to a person")
    @has_permissions(kick_members=True)
    async def send(self, ctx, member: Member = None, *, message):
        if member is None:
            await ctx.send("Please provide a member to send a message to")
        if message is None:
            await ctx.send("Please provide a message to send to the user")
        sEmbed = Embed(title="Message from the Mods", description=f"Message sent by {ctx.author.display_name}")
        sEmbed.add_field(name="Content of the message", value=message)
        await ctx.send(embed=sEmbed)

    @command(name='kick', pass_context=True, help='kick a user')
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: Member = None, *reason):
        if reason is None:
            return await ctx.send("Please provide a valid reason for kicking the member")
        true_reason = ' '.join(reason)
        if member == ctx.author:
            return await ctx.send("Oye stop kicking yourself")
        elif member is None:
            return await ctx.send("Please provide a valid member to kick")
        else:
            await member.kick(reason=true_reason)
            await ctx.send(f"{member.mention} has been kicked from the server {ctx.guild.name} for {true_reason}")

    @command(name='ban', pass_context=True, help='ban a user')
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: Member = None, *reason):
        if reason is None:
            return await ctx.send("Please provide a valid reason")
        if member == ctx.author:
            return await ctx.send("Oye stop kicking yourself")
        elif member is None:
            return await ctx.send("Please provide a valid member to ban")
        else:
            true_reason = ' '.join(reason)
            await member.ban(reason=true_reason)
            await ctx.send(f"{member.mention} has been banned from the server.")

    @command(name='unban', pass_context=True, help='unban a user')
    @has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_disc):
                await ctx.guild.unban(user)
                await ctx.send(f"{user} was unbanned")

    @command(name='purge', pass_context=True, aliases=['clear'], help="Clear a certain number of messages.")
    async def clear(self, ctx, limit: int = None):
        if limit is None:
            return await ctx.send("Please specify the number of messages to delete")
        elif limit > 100:
            return await ctx.send("Too many messages to purge")
        else:
            await ctx.channel.purge(limit=limit)
            message = await ctx.send(f"Purged {limit} messages")
            await asyncio.sleep(5)
            await message.delete()

    @command(name='lock', pass_context=True, help="Lock a channel")
    async def lock(self, ctx, channel: Optional[TextChannel], reason=None):
        if reason is None:
            return await ctx.send("You have not provided a reason to lock the channel")
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = Embed(title="The channel has been locked",
                   description=f"The channel has been locked. Reason: `{reason}`", colour=Colour.blurple())
        await ctx.send(embed=em)

    @command(name='unlock', pass_context=True, help="Unlock a channel")
    async def unlock(self, ctx, channel: TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send("Channel unlocked")

    @command(name='lockdown', pass_context=True, help="Lock all the channels in a server")
    async def lockdown(self, ctx, end: Optional[str]):
        if end is None:
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send("The server has been locked")
        else:
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            await ctx.send("The server has been unlocked")

    @command(name="mute", pass_context=True, help="Add the muted role to a person")
    async def mute(self, ctx, member: Member = None):
        if Member is None:
            return await ctx.send("You have not mentioned a member to mute")
        mutedRole = get(ctx.guild.roles, name="Muted")
        if mutedRole is None:
            return await ctx.send("You need to create a muted role")
        else:
            await member.add_roles(mutedRole)
            await ctx.send(f"{member.display_name} has been muted")

    @command(name="unmute", pass_context=True, help="Remove the muted role from a person")
    async def unmute(self, ctx, member: Member = None):
        if Member is None:
            return await ctx.send("You have not mentioned a member to unmute")
        mutedRole = get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedRole)
        await ctx.send(f"{member.display_name} has been unmuted")


def setup(bot):
    bot.add_cog(Moderation(bot))
