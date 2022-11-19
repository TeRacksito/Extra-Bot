import nextcord, sys
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
sys.path.insert(1, 'cogs\lib')
import values as v

guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Kick command
    @nextcord.slash_command(guild_ids=guilds, description="Kick The Specified Member", force_global = True)
    @has_permissions(kick_members=True)
    async def kick(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason: str = nextcord.SlashOption(description="The Reason You Want To Kick The Member", required=True)):
        await interaction.response.defer() 
        await member.send(f"You Got Kick From The Server \nReason:{reason}")
        await member.kick(reason=reason)
        await interaction.followup.send(f"Kicked {member}\nReason:{reason}")

    # Exeption in case if the member doen't have the permissions
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You Don't Have The Permissions To Kick !")

    @nextcord.slash_command(guild_ids=guilds, description="Ban Sepcified Member", force_global = True)
    @has_permissions(ban_members=True)
    async def ban(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason: str = nextcord.SlashOption(description="The Reason You Want To Ban The Member", required=True)):
        await interaction.response.defer()
        await member.send(f"You Got Ban From The Server \nReason:{reason}")
        await member.ban(reason=reason)
        await interaction.followup.send(f"Banned {member}\nReason:{reason}")

    @ban.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You Don't Have The Permissions To Ban !")

# Setup
def setup(client):
    client.add_cog(Moderation(client))
