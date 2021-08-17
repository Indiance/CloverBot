from discord import Embed
from discord.ext.commands import command, Cog
import requests
import html
import random
import os
from dotenv import load_dotenv
from discord_components import DiscordComponents, Button, ButtonStyle
from asyncio import TimeoutError
load_dotenv()

key = os.getenv("QUIZ_TOKEN")

class Trivia(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.bot)

    @command(name="trivia", pass_context=True, help="Play a game of trivia where you can choose the difficulty between easy difficult and hard")
    async def trivia(self, ctx, difficulty: str = None):
        if difficulty is None:
            url = "https://opentdb.com/api.php?amount=1"
        else:
            url = f"https://opentdb.com/api.php?amount=1&difficulty={difficulty.lower()}"
        r = requests.get(url)
        results = r.json()["results"][0]
        category = results["category"]
        difficulty = results["difficulty"]
        question = html.unescape(results["question"])
        correct_answer = html.unescape(results["correct_answer"])
        incorrect_answers = [html.unescape(
            incorrect_answer) for incorrect_answer in results["incorrect_answers"]]
        triviaEmbed = Embed(title=f"Question for {ctx.author.display_name}",
                            description=f"**Category**: {category} **Difficulty**: {difficulty}", color=ctx.author.color)
        options = " "
        answers = incorrect_answers + [correct_answer]
        random.shuffle(answers)
        for thing in answers:
            options += f"{thing}\n"
        triviaEmbed.add_field(name="Question", value=question, inline=False)
        triviaEmbed.add_field(name="Options", value=options, inline=False)
        msg = await ctx.send(
             embed=triviaEmbed,
             components=[[Button(style=ButtonStyle.blue, label=answer) for answer in answers]])
        try:
             interaction = await self.bot.wait_for("button_click")
             if interaction.component.label in incorrect_answers:
                 await interaction.respond(type=6)
                 await msg.edit(
                     components=[[Button(style=ButtonStyle.green, label=ans) if ans == correct_answer else Button(
                         style=ButtonStyle.red, label=ans) for ans in answers]]
                 )
                 await ctx.send("That was the wrong answer")
             else:
                 await interaction.respond(type=6)
                 await msg.edit(
                     components=[[Button(style=ButtonStyle.green, label=ans) if ans == correct_answer else Button(
                         style=ButtonStyle.red, label=ans) for ans in answers]]
                 )
                 await ctx.send("That was the right answer")
        except TimeoutError:
             await ctx.send("No answer received in time")

def setup(bot):
    bot.add_cog(Trivia(bot))