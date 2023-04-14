"""
ping cog module

Implements `Ping cog class`.
"""
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from cooldowns import define_shared_cooldown, shared_cooldown, SlashBucket, CallableOnCooldown

from cogs.lib.values import DataFetcher as DF

guilds= DF.get("guilds")
embeds = DF.get("embeds")
embedColor= embeds["default"]["color"]

class Ping(commands.Cog):
    """
    ping cog class

    Implements latency slash commands.
    """
    define_shared_cooldown(2, 8, SlashBucket.author, cooldown_id="Ping_cooldown")

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids= guilds, force_global= True,
                            description= "Gives you the current ping of the bot")
    @shared_cooldown("Ping_cooldown")
    async def ping(self, interaction: Interaction):
        """
        ping slash command

        Sends an embed with current latency information.
        """
        await interaction.response.defer()
        data_embed = nextcord.Embed(title= "Pong!", color= embedColor,
                                    description= f"The bot's ping is {round(self.bot.latency * 1000)}ms")
        await interaction.followup.send(embed= data_embed)

    @ping.error
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
    bot.add_cog(Ping(bot))
