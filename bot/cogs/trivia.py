from discord import Embed
from discord.ext.commands import command, Cog
import requests
import html
import random
import os
from dotenv import load_dotenv
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption
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
        categories = {
            "General Knowledge":"9",
            "Books":"10",
            "Film":"11",
            "Music":"12",
            "Musicals & Theatres":"13",
            "Television":"14",
            "Videogames":"15",
            "Boardgames": "16",
            "Science and Nature": "17",
            "Computers":"18",
            "Mathematics":"19",
            "Mythology":"20",
            "Sports":"21",
            "Geography":"22",
            "History":"23",
            "Politics":"24",
            "Art":"25",
            "Celebrities":"26",
            "Animals":"27",
            "Vehicles":"28",
            "Comics":"29",
            "Gadgets":"30",
            "Anime and Manga":"31",
            "Cartoon and Animations":"32"
        }
        msg = await ctx.send("Choose a category",components = [
            Select(placeholder="Select something", options=[SelectOption(label=x[0], value=x[1]) for x in categories.items()])
        ])
        try:
            interaction = await self.bot.wait_for("select_option", check=lambda inter: inter.user.id == ctx.author.id)
            await interaction.respond(type=6)
            await msg.edit("Choose a category",components = [
            Select(placeholder="Select something", options=[SelectOption(label=x[0], value=x[1]) for x in categories.items()], disabled=True)
        ])
            if difficulty is None:
                url = f"https://opentdb.com/api.php?amount=1&category={interaction.values[0]}"
            else:
                url = f"https://opentdb.com/api.php?amount=1&difficulty={difficulty.lower()}&category={interaction.values[0]}"
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
                interaction = await self.bot.wait_for("button_click", check = lambda i: i.user.id == ctx.author.id)
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
                        components=[[Button(style=ButtonStyle.green, label=ans, disabled=True) if ans == correct_answer else Button(
                            style=ButtonStyle.red, label=ans, disabled=True) for ans in answers]]
                    )
                    await ctx.send("That was the right answer")
            except TimeoutError:
                await ctx.send("No answer received in time")
        except TimeoutError:
            await ctx.send("No response was given in time")


def setup(bot):
    bot.add_cog(Trivia(bot))
