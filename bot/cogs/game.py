from discord.ext.commands import command, Cog
from asyncio import TimeoutError
from random import choice

class Game(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name="rps", pass_context=True, help="Play some rock paper scissors")
    async def rps(self, ctx):
        rock = "🪨"
        paper = "📰"
        scissors = "✂️"
        rps = [rock, paper, scissors]
        msg = await ctx.send('Pick your choice')
        for reaction in rps:
            await msg.add_reaction(reaction)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in rps
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except TimeoutError:
            await ctx.send('A response was not given in time')
        else:
            oppn_choice = choice(rps)
            reaction = str(reaction.emoji)
            if reaction == oppn_choice:
                await ctx.send("You both drew")
            if oppn_choice == rock:
                if reaction == scissors:
                    await ctx.send("You lose!")
                if reaction == paper:
                    await ctx.send("You win!")
            if oppn_choice == paper:
                if reaction == rock:
                    await ctx.send("You lose!")
                if reaction == scissors:
                    await ctx.send("You win!")
            if oppn_choice == scissors:
                if reaction == paper:
                    await ctx.send("You lose!")
                if reaction == rock:
                    await ctx.send("You win!")
            await ctx.send(f"The opponent chose {oppn_choice}")

def setup(bot):
    bot.add_cog(Game(bot))