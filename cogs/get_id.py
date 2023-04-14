"""
get_id cog module

Implements `GetID cog class`.
"""
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from cooldowns import define_shared_cooldown, shared_cooldown, SlashBucket, CallableOnCooldown

from cogs.lib.values import DataFetcher as DF

guilds= DF.get("guilds")
embeds = DF.get("embeds")
embedColor= embeds["default"]["color"]

class GetID(commands.Cog):
    """
    GetID cog class

    Implements slash commands for users information retrieving.
    """
    define_shared_cooldown(2, 8, SlashBucket.author, cooldown_id="GetID_cooldown")

    def __init__(self, bot):
        self.bot = bot

    # Get ID Command Self Explanatory
    @nextcord.slash_command(guild_ids= guilds, force_global= True, dm_permission= True,
                            description= "Get The Id Of A Specific Member")
    @shared_cooldown("GetID_cooldown")
    async def getpfp(self, interaction: Interaction, user: nextcord.User):
        """
        getpfp slash command

        Sends an embed with information about given user.
        Get Profile Picture.

        Parameters
        ----------
        user : `nextcord.User`
            Where information is extracted from.
        """
        await interaction.response.defer()
        id_embed = nextcord.Embed(
            title= f"{user.name}'s Id",
            color= embedColor,
            description= f"The Id Of `{user.name}#{user.discriminator}` is {user.id}")
        try:
            id_embed.set_thumbnail(user.avatar.url)
            id_embed.add_field(name= "Avatar download link", value= f"[Click Here]({user.avatar.url})")
        except AttributeError:
            pass
        id_embed.add_field(name= "Joined Discord on", value= user.created_at)
        await interaction.followup.send(embed= id_embed)

    @nextcord.slash_command(guild_ids= guilds, description= "Tell You Your Id In Discord")
    @shared_cooldown("GetID_cooldown")
    async def myid(self, interaction: Interaction):
        """
        myid slash command

        Sends the interaction.user's ID.
        """
        await interaction.response.defer()
        await interaction.followup.send(f"{interaction.user.id} Is Your Id")

    @getpfp.error
    @myid.error
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
    bot.add_cog(GetID(bot))
