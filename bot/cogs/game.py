from discord.ext.commands import command, Cog
from asyncio import TimeoutError
from random import choice
from discord_components import Button, ButtonStyle

class Game(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command(name="rps", pass_context=True, help="Play some rock paper scissors")
    async def rps(self, ctx):
        rock = "🪨"
        paper = "📰"
        scissors = "✂️"
        rps = [rock, paper, scissors]
        msg = await ctx.send('Pick your choice', components = [[Button(label=object) for object in rps]])
        interaction = await self.bot.wait_for("button_click")
        try:
            reaction = interaction.component.label
            await msg.edit(
                     components=[[Button(style=ButtonStyle.blue, label=reaction) if object == reaction else Button(
                         label=object) for object in rps]]
                 )
            await interaction.respond(type=6)
            oppn_choice = choice(rps)
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
        except TimeoutError:
            await ctx.send("No response was sent in time")

def setup(bot):
    bot.add_cog(Game(bot))