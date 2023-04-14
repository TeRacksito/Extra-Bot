"""
meme cog module

Implements `Memes cog class`.
"""
import datetime

import nextcord
from cooldowns import define_shared_cooldown, shared_cooldown, SlashBucket, CallableOnCooldown
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
    define_shared_cooldown(2, 8, SlashBucket.author, cooldown_id="Memes_cooldown")

    def __init__(self, bot):
        self.bot = bot
        # A custom hand-crafted basic cooldown. Affects the whole meme command, everywhere.
        self.cooldown = datetime.datetime(1, 1, 1)

    @nextcord.slash_command(guild_ids= guilds, force_global = True, dm_permission = True,
                            description= "Generates an SFW meme and sends it to the chat, this command sometimes works and sometimes not")
    @shared_cooldown("Memes_cooldown")
    async def meme(self, interaction: Interaction):
        """
        meme slash command

        Uses a meme API to generate a random meme and send it on a embed.
        """
        await interaction.response.defer()
        if (datetime.datetime.now() - self.cooldown).total_seconds() >= 30:
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
                # Custom cooldown is applied.
                await interaction.followup.send("Oops, something went wrong. Unable to get the meme you wanted.\n"+
                                        "Try again later, but if the error persists is probable that the Meme API is down.")
                self.cooldown = datetime.datetime.now()
                return None
        else:
            # Custom cooldown handler.
            retry_after = round(30 - (datetime.datetime.now() - self.cooldown).total_seconds(), 2)
            await interaction.followup.send("Oops, cooldown for memes was applied.\n"+
                                      f"Try again in {retry_after} seconds.")
            return None

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
