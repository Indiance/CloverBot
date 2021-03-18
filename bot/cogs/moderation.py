import discord
from discord.ext import commands
import aiofiles

bot_warnings = {}


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        game = discord.Game('+help')
        await self.bot.change_presence(activity=game)
        for guild in self.bot.guilds:
            async with aiofiles.open(f"{guild.id}.txt", mode="a") as temp:
                pass
            bot_warnings[guild.id] = {}

        for guild in self.bot.guilds:
            async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
                lines = await file.readlines()

                for line in lines:
                    data = line.split(" ")
                    member_id = int(data[0])
                    admin_id = int(data[1])
                    reason = " ".join(data[2:]).strip("\n")
                    try:
                        bot_warnings[guild.id][member_id][0] += 1
                        bot_warnings[guild.id][member_id][1].append(
                            (admin_id, reason))
                    except KeyError:
                        bot_warnings[guild.id][member_id] = [
                            1, [(admin_id, reason)]]

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        bot_warnings[guild.id] = {}

    @commands.command(name='kick', pass_context=True, help='kick a user')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *reason):
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

    @commands.command(name='ban', pass_context=True, help='ban a user')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *reason):
        if reason is None:
            return await ctx.send("Please provide a valid reason")
        if member == ctx.author:
            return await ctx.send("Oye stop kicking yourself")
        elif member is None:
            return await ctx.send("Please provide a valid member to ban")
        else:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} has been banned from the server.")

    @commands.command(name='unban', pass_context=True, help='unban a user')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_disc):
                await ctx.guild.unban(user)
                await ctx.send(f"{user} was unbanned")

    @commands.command(name='warn', pass_context=True, help='warn the user')
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member = None, reason=None):
        if member is None:
            return await ctx.send("The member you have provided is not found or you have not provided a member.")

        if member is self.bot.user:
            return await ctx.send("Oye stop warning me")

        if reason is None:
            return await ctx.send("Please provide a reason for warning the member.")

        try:
            first_warning = False
            bot_warnings[ctx.guild.id][member.id][0] += 1
            bot_warnings[ctx.guild.id][member.id][1].append(
                (ctx.author.id, reason))
        except KeyError:
            first_warning = True
            bot_warnings[ctx.guild.id][member.id] = [
                1, [(ctx.author.id, reason)]]

        count = bot_warnings[ctx.guild.id][member.id][0]

        async with aiofiles.open(f"{member.guild.id}.txt", mode="a") as file:
            await file.write(f"{member.id} {ctx.author.id} {reason}\n")

        await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")

    @commands.command(name='warnings', pass_context=True, help='show the warnings of a person')
    async def warnings(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("The member you have provided is not found or you have not provided a vallid member.")

        warnEmbed = discord.Embed(
            title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())

        try:
            i = 1
            for admin_id, reason in bot_warnings[ctx.guild.id][member.id][1]:
                admin = member.guild.get_member(admin_id)
                warnEmbed.description += f"**Warning {i}** given by: {admin.mention} for *'{reason}'*.\n"
                i += 1
            await ctx.send(embed=warnEmbed)
        except KeyError:
            await ctx.send("This member has no warnings")

    @commands.command(name='clearwarns', pass_context=True, help='clear the warnings of a person')
    async def clearwarns(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send("The member you have provided is invalid or you have not provided one")
        try:
            del bot_warnings[ctx.guild.id][member.id]
        except KeyError:
            return await ctx.send("This person does not have any warnings to clear.")

        with open(f"{ctx.guild.id}.txt", "r") as file:
            lines = file.readlines()

        with open(f"{ctx.guild.id}.txt", mode="w") as file:
            for line in lines:
                if str(member.id) not in line:
                    file.write(line)


def setup(bot):
    bot.add_cog(Moderation(bot))
