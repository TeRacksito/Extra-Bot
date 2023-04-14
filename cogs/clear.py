"""
clear cog module

Implements `Clear cog class`.
"""

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from cooldowns import define_shared_cooldown, shared_cooldown, SlashBucket, CallableOnCooldown

from cogs.lib.values import DataFetcher as DF

guilds= DF.get("guilds")

class Clear(commands.Cog):
    """
    Clear cog class
    
    Implements channel's messages management slash commands.
    """
    define_shared_cooldown(2, 8, SlashBucket.author, cooldown_id="Clear_cooldown")

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids= guilds, description= "Clears a number of messages specified", force_global= True)
    @shared_cooldown("Clear_cooldown")
    async def clear(self, interaction: Interaction,
                    number: int = SlashOption(required= False, default= 20,
                                              description= "Number Of Messages You Want To Delete, 20 by default")):
        """
        clear slash command

        This slash command purges a given amount of messages in the Interaction's channel.

        Parameters
        ----------
        number : `int, optional`
            The number of messages to be purged, by default 20.
        """
        def is_interaction_message(message: nextcord.Message):
            """
            is_interaction_message function

            Checks if the message is the `interaction.response.defer()` one.
            Returns False if so on.
            """
            # pylint: disable=invalid-name
            # pylint: disable=global-variable-undefined
            global already_caught
            try:
                if (message.type is message.type.chat_input_command and message.content == "" and message.flags.value == 128):
                    # pylint: disable=used-before-assignment
                    if already_caught != message:
                        return True
                else:
                    return True
            except NameError:
                already_caught = message
                return False
        await interaction.response.defer()

        # +1 is added to number because the interaction.response.defer message also counts.
        purged_messages = await interaction.channel.purge(limit= number +1, bulk= True, check= is_interaction_message)
        try:
            bot_message: nextcord.Message = await interaction.followup.send(f"```Successfully deleted {len(purged_messages)} messages```")
        except nextcord.errors.NotFound:
            bot_message: nextcord.Message = await interaction.channel.send(f"```Successfully deleted {len(purged_messages)} messages```")
        await bot_message.delete(delay= 3)

    @clear.error
    async def on_cooldown(self, interaction: Interaction, error: nextcord.ApplicationError):
        """
        on_cooldown function

        Generic on cooldown handler.
        """
        if isinstance(error, CallableOnCooldown):
            await interaction.send(ephemeral= True,
                                   content= f"You are being rate-limited! Retry in `{round(error.retry_after, 2)}` seconds.")
# Setup
def setup(bot: commands.Bot):
    # pylint: disable=missing-function-docstring
    bot.add_cog(Clear(bot))
