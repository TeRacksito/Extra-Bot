"""
moderation cog module

Implements `Moderation cog class`.
"""
import nextcord
from nextcord import Interaction, SlashOption, ApplicationCheckFailure
from nextcord.ext import commands, application_checks

from cooldowns import define_shared_cooldown, shared_cooldown, SlashBucket, CallableOnCooldown

from cogs.lib.values import DataFetcher as DF

guilds= DF.get("guilds")

class Moderation(commands.Cog):
    """
    Moderation cog class

    Implements moderation slash commands such as `kick` and `ban`.
    """
    define_shared_cooldown(2, 8, SlashBucket.author, cooldown_id="Moderation_cooldown")

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(guild_ids= guilds, force_global= True,
                            description= "Kick The Specified Member")
    @application_checks.has_permissions(kick_members= True)
    @shared_cooldown("Moderation_cooldown")
    async def kick(self, interaction: Interaction, member: nextcord.Member, *,
                   reason: str = SlashOption(description= "The Reason You Want To Kick The Member", required= True)):
        """
        kick slash command

        Attempts to kick a given member.

        Parameters
        ----------
        member : `nextcord.Member`
            The member to be kicked.
        reason : `str`
            The reason of kicking the given member.
        """
        await interaction.response.defer()
        await member.send(f"You Got Kick From The Server\nReason:{reason}")
        await member.kick(reason= reason)
        await interaction.followup.send(f"Kicked {member}\nReason:{reason}")

    @nextcord.slash_command(guild_ids= guilds, force_global= True,
                            description= "Ban Specified Member")
    @application_checks.has_permissions(ban_members= True)
    @shared_cooldown("Moderation_cooldown")
    async def ban(self, interaction: Interaction, member: nextcord.Member, *,
                  reason: str = SlashOption(description= "The Reason You Want To Ban The Member", required= True)):
        """
        ban slash command

        Attempts to ban a given member.

        Parameters
        ----------
        member : `nextcord.Member`
            The member to be banned.
        reason : `str`
            The reason of banning the given member.
        """
        await interaction.response.defer()
        await member.send(f"You Got Ban From The Server\nReason:{reason}")
        await member.ban(reason= reason)
        await interaction.followup.send(f"Banned {member}\nReason:{reason}")

    @kick.error
    @ban.error
    async def generic_error(self, interaction: Interaction, error: nextcord.ApplicationError):
        """
        generic_error handler

        Handles the exception raised when `interaction.user` does not have the required
        permisiones to perform the `kick` or `ban` slash command.

        Also handles the on cooldown error.
        """
        if isinstance(error, ApplicationCheckFailure):
            await interaction.send("You Don't Have The Necessary Permissions!")
        elif isinstance(error, CallableOnCooldown):
            await interaction.send(ephemeral= True,
                                   content= f"You are being rate-limited! Retry in `{round(error.retry_after, 2)}` seconds.")
# Setup
def setup(bot):
    # pylint: disable=missing-function-docstring
    bot.add_cog(Moderation(bot))
