"""
cubing cog module

Implements `Cubing cog class`.
"""
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from pyTwistyScrambler import scrambler333

from cooldowns import define_shared_cooldown, shared_cooldown, SlashBucket, CallableOnCooldown

from cogs.lib.values import DataFetcher as DF

guilds = DF.get("guilds")
embeds = DF.get("embeds")
embedColor = embeds["default"]["color"]

class Cubing(commands.Cog):
    """
    Cubing cog class

    Implements Rubik's cube slash commands.
    """
    define_shared_cooldown(2, 8, SlashBucket.author, cooldown_id="Cubing_cooldown")

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids= guilds, force_global= True,
                            description= "Generate a rubik's cube scramble using the Official WCA format")
    @shared_cooldown("Cubing_cooldown")
    async def gen_scramble(self, interaction: Interaction):
        """
        gen_scramble slash command

        Generates WCA scramble of a 3x3x3 Rubik's cube. Sends it as a Embed.
        """
        await interaction.response.defer()
        scramble = scrambler333.get_WCA_scramble()
        embed = nextcord.Embed(title= "Rubik's Cube scramble", color= embedColor,
                               description= f"Here's the generated Scramble\n```{scramble}```")
        await interaction.followup.send(embed= embed)

    @nextcord.slash_command(guild_ids= guilds, force_global= True,
                            description= "Generates a scramble for the last layer, useful for training OLL")
    @shared_cooldown("Cubing_cooldown")
    async def last_layer_scramble(self, interaction: Interaction):
        """
        last_layer_scramble slash command

        Generates the last layer scramble of a 3x3x3 Rubik's cube. Sends it as a Embed.
        """
        await interaction.response.defer()
        scramble = scrambler333.get_LL_scramble()
        embed = nextcord.Embed(title= "Last Layer scramble", color= embedColor,
                               description= f"Here's the generated Last Layer Scramble\n```{scramble}```")
        await interaction.followup.send(embed= embed)

    @nextcord.slash_command(guild_ids= guilds, force_global= True,
                            description= "Generates a scramble that has the cross only solved, useful for training F2L")
    @shared_cooldown("Cubing_cooldown")
    async def f2l_scramble(self, interaction: Interaction):
        """
        f2l_scramble slash command

        Same as `last_layer_scramble` slash command. A bug probably?
        """
        await interaction.response.defer()
        scramble = scrambler333.get_LL_scramble()
        embed = nextcord.Embed(title= "Cross solved only scramble", color= embedColor,
                               description= f"Here's the generated Scramble\n```{scramble}```")
        await interaction.followup.send(embed= embed)

    @gen_scramble.error
    @last_layer_scramble.error
    @f2l_scramble.error
    async def on_cooldown(self, interaction: Interaction, error: nextcord.ApplicationError):
        """
        on_cooldown function

        Generic on cooldown handler.
        """
        if isinstance(error, CallableOnCooldown):
            await interaction.send(ephemeral= True,
                                   content= f"You are being rate-limited! Retry in `{round(error.retry_after, 2)}` seconds.")
# Setup
def setup(bot):
    # pylint: disable=missing-function-docstring
    bot.add_cog(Cubing(bot))
