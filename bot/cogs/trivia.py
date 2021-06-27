from discord import Embed
from discord.ext.commands import command, Cog, cooldown, BucketType, CommandOnCooldown
import requests
import os
from discord_components import DiscordComponents, Button, ButtonStyle
from dotenv import load_dotenv
import asyncio
import html
import random

load_dotenv()

key = os.getenv("QUIZ_TOKEN")


class Trivia(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="trivia", pass_context=True, help="Play a game of trivia where you can choose the difficulty between easy difficult and hard")
    @cooldown(1, 20, BucketType.user)
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
            btn1 = await self.bot.wait_for("button_click")
            if btn1.component.label in incorrect_answers:
                await btn1.respond(type=6)
                await msg.edit(
                    components=[[Button(style=ButtonStyle.green, label=ans) if ans == correct_answer else Button(
                        style=ButtonStyle.red, label=ans) for ans in answers]]
                )
                await ctx.send("That was the wrong answer")
            else:
                await btn1.respond(type=6)
                await msg.edit(
                    components=[[Button(style=ButtonStyle.green, label=ans) if ans == correct_answer else Button(
                        style=ButtonStyle.red, label=ans) for ans in answers]]
                )
                await ctx.send("That was the right answer")
        except asyncio.TimeoutError:
            await ctx.send("No answer received in time")

    @trivia.error
    async def trivia_error(self, ctx, err):
        if isinstance(err, CommandOnCooldown):
            await ctx.send(f"Oops that command is on cooldown for {err.retry_after:.0f} more seconds")


def setup(bot):
    DiscordComponents(bot)
    bot.add_cog(Trivia(bot))
