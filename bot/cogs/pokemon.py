# discord Imports
from discord import Embed
from discord.ext.commands import command, Cog
# import pokemon thingy
import pokebase as pb


class Pokemon(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="pokemon", pass_context=True, help="Obtain information about a pokemon")
    async def pokemon(self, ctx, pokemon=None):
        if pokemon is None:
            return await ctx.send("Please provide a pokemon to display information about")
        try:
            data = pb.pokemon(pokemon)
        except:
            return await ctx.send("The pokemon could not be found")

        pokemon_avatar = pb.SpriteResource('pokemon', data.id).url
        pokeEmbed = Embed()
        pokeEmbed.color = ctx.author.color
        pokeEmbed.title = f"Showing data about {data.name.title()}"
        pokeEmbed.url = f"https://bulbapedia.bulbagarden.net/wiki/{pokemon.title()}_(Pokémon)"
        pokeEmbed.set_footer(
            text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        pokeEmbed.set_thumbnail(url=pokemon_avatar)
        pokeEmbed.add_field(name="Pokedex Number", value=data.id)
        pokeEmbed.add_field(name="Height", value=f"{data.height} decimeters")
        pokeEmbed.add_field(name="Weight", value=f"{data.weight} hectograms")
        pokeEmbed.add_field(name="Types", value=", ".join(
            [type.type.name.title() for type in data.types]))
        pokeEmbed.add_field(name="Base HP", value=data.stats[0].base_stat, inline=True)
        pokeEmbed.add_field(name="Base Attack", value=data.stats[1].base_stat, inline=True)
        pokeEmbed.add_field(name="Base Defense", value=data.stats[2].base_stat, inline=True)
        pokeEmbed.add_field(name="Base Special Attack", value=data.stats[3].base_stat, inline=True)
        pokeEmbed.add_field(name="Base Special Defense", value=data.stats[4].base_stat, inline=True)
        pokeEmbed.add_field(name="Base Speed", value=data.stats[5].base_stat, inline=True)
        pokeEmbed.add_field(name="Evolves From Species", value=data.species.evolves_from_species, inline=True)
        await ctx.send(embed=pokeEmbed)


def setup(bot):
    bot.add_cog(Pokemon(bot))
