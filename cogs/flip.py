"""
flip cog module

Implements `FlipCoin cog class`.
"""
import random

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from cooldowns import define_shared_cooldown, shared_cooldown, SlashBucket, CallableOnCooldown

from cogs.lib.values import DataFetcher as DF

guilds= DF.get("guilds")

class FlipCoin(commands.Cog):
    """
    flipcoin cog class

    Implements flipping coins slash commands.
    """
    define_shared_cooldown(2, 8, SlashBucket.author, cooldown_id="FlipCoin_cooldown")

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids= guilds, description= "Flips a coin", force_global= True)
    @shared_cooldown("FlipCoin_cooldown")
    async def flipcoin(self, interaction: Interaction):
        """
        flipcoin slash command

        Flips a coin and send the result mentioning the interaction.user.
        """
        await interaction.response.defer()
        choices = ["heads", "tails"]
        random.shuffle(choices)
        final_choice = random.choice(choices)
        await interaction.followup.send(f"<@{interaction.user.id}> {final_choice}")

    @flipcoin.error
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
    bot.add_cog(FlipCoin(bot))
