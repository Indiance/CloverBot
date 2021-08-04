from discord import Embed
from discord.ext.commands import command, Cog, cooldown, BucketType, CommandOnCooldown
import requests
import html
import random
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("QUIZ_TOKEN")

class Trivia(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="trivia", pass_context=True, help="Play a game of trivia where you can choose the difficulty between easy difficult and hard")
    @cooldown(1, 20, BucketType.user)
    async def trivia(self, ctx, difficulty: str = None):
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
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
            options += f"{emojis[answers.index(thing)]} {thing}\n"
        triviaEmbed.add_field(name="Question", value=question, inline=False)
        triviaEmbed.add_field(name="Options", value=options, inline=False)
        msg = await ctx.send(embed=triviaEmbed)
        for i in range(len(answers)):
            await msg.add_reaction(emojis[i])

        reaction = await self.bot.wait_for('reaction_add')
        user_answer = answers[emojis.index(reaction[0].emoji)]
        if user_answer == correct_answer:
            await ctx.send("You got it right!")
        else:
            await ctx.send(f"You got it wrong! The correct answer was ***{correct_answer}***")



    @trivia.error
    async def trivia_error(self, ctx, err):
        if isinstance(err, CommandOnCooldown):
            await ctx.send(f"Oops that command is on cooldown for {err.retry_after:.0f} more seconds")


def setup(bot):
    bot.add_cog(Trivia(bot))
