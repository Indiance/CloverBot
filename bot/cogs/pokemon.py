# discord Imports
from discord import Embed
from discord.ext.commands import command, Cog

# import pokemon thingy
import pokepy


class Miscellaneous(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="pokemon", pass_context=True)
    async def pokemon(self, ctx, pokemon=None):
        if pokemon is None:
            return await ctx.send("Please provide a pokemon to display information about")
        client = pokepy.V2Client()
        if pokemon.isnumeric():
            try:
                data = client.get_pokemon(int(pokemon)[0])
            except:
                return await ctx.send("The pokemon could not be found")
        else:
            try:
                data = client.get_pokemon(pokemon)[0]
            except:
                return await ctx.send("The pokemon could not be found")

        pokemon_avatar = data.sprites.front_default
        pokeEmbed = Embed()
        pokeEmbed.color = ctx.author.color
        pokeEmbed.title = f"Showing data about {data.name.title()}"
        pokeEmbed.url = f"https://bulbapedia.bulbagarden.net/wiki/{pokemon.title()}_(Pokémon)"
        pokeEmbed.set_footer(
            text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        pokeEmbed.set_thumbnail(url=pokemon_avatar)
        pokeEmbed.add_field(name="Pokedex Number", value=data.id)
        pokeEmbed.add_field(name="Height", value=data.height)
        pokeEmbed.add_field(name="Weight", value=data.weight)
        pokeEmbed.add_field(name="Types", value=", ".join(
            [type.type.name.title() for type in data.types]))
        pokeEmbed.add_field(name="Abilities", value=", ".join(
            [ability.ability.name.title() for ability in data.abilities]))
        try:
            evolution = client.get_pokemon_species(
                pokemon)[0].evolves_from_species.name
            pokeEmbed.add_field(name="Evolves from", value=evolution)
        except:
            pokeEmbed.add_field(name="Evolves from", value="None")
        await ctx.send(embed=pokeEmbed)


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
