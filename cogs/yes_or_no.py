"""
yes_or_no cog module

Implements `YesOrNo cog class`.
"""
from random import choice, shuffle

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from cooldowns import define_shared_cooldown, shared_cooldown, SlashBucket, CallableOnCooldown

from cogs.lib.values import DataFetcher as DF

guilds = DF.get("guilds")
embeds = DF.get("embeds")
embedColor = embeds["default"]["color"]

class YesOrNo(commands.Cog):
    """
    YesOrNo cog class

    Implements random answering slash commands.
    """
    define_shared_cooldown(2, 8, SlashBucket.author, cooldown_id="YesOrNo_cooldown")

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids= guilds, force_global= True,
                            description= "Yes Or No Command Ask the bot a question")
    @shared_cooldown("YesOrNo_cooldown")
    async def yesorno(self, interaction: Interaction,
                      question: str = SlashOption(description= "Question", required= True)):
        """
        yesorno slash command

        Choses randomly between an affirmative and negative answers for
        given yes or no question.

        Parameters
        ----------
        question : `str`
            The question to be randomly answered.
        """
        await interaction.response.defer()
        answers = ["Yes", "No", "Of Course", "Of Course ||No||", "I Can't Decide","是的，但是中文","不"]
        shuffle(answers)
        embed = nextcord.Embed(title= question, description= f"{choice(answers)}", color= embedColor)
        await interaction.followup.send(embed= embed)

    @yesorno.error
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
    bot.add_cog(YesOrNo(bot))
