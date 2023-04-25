"""
meme cog module

Implements `Memes cog class`.
"""

import nextcord
from cooldowns import CallableOnCooldown, SlashBucket, TriggerCooldown
from nextcord import Interaction
from nextcord.ext import commands
from requests.exceptions import Timeout

from cogs.lib.meme_api import gen_meme
from cogs.lib.values import DataFetcher as DF

guilds= DF.get("guilds")
embeds= DF.get("embeds")
embedColor= embeds["default"]["color"]

class Memes(commands.Cog):
    """
    Memes cog class

    Implements meme slash commands.
    """
    my_trigger_cooldown = TriggerCooldown(2, 10, SlashBucket.author)

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids= guilds, force_global = True, dm_permission = True,
                            description= "Generates an SFW meme and sends it to the chat, this command sometimes works and sometimes not")
    @my_trigger_cooldown
    async def meme(self, interaction: Interaction):
        """
        meme slash command

        Uses a meme API to generate a random meme and send it on a embed.
        """
        await interaction.response.defer()
        try:
            meme = gen_meme()
            meme_embed = nextcord.Embed(title= "Here's a meme", color= embedColor)
            meme_embed.set_image(url= meme)
            meme_embed.url = "https://github.com/D3vd/Meme_Api"
            meme_embed.set_footer(icon_url= "https://cdn.discordapp.com/attachments/1027493896055439360/1068564499763830804/GitHub-Mark.png",
                                text= "Powered by Meme API on Github ==>\n"+
                                        "https://github.com/D3vd/Meme_Api")
            await interaction.followup.send(embed= meme_embed)
        except Timeout:
            await self.my_trigger_cooldown.trigger(40)


    @meme.error
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
    bot.add_cog(Memes(bot))
