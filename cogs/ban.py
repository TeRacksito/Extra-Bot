from code import interact
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from configparser import ConfigParser

config=ConfigParser()
config.read(".\config.ini")
guild_id_1=config["options"]["guild1_id"]
guild_id_2=config["options"]["guild2_id"]
guilds=[int(guild_id_1),int(guild_id_2)]

class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ban command
    @nextcord.slash_command(guild_ids=guilds, description="Ban Sepcified Member")
    @has_permissions(ban_members=True)
    async def ban(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason: str = nextcord.SlashOption(description="The Reason You Want To Ban The Member", required=True)):
        await member.send(f"You Got Ban From The Server \nReason:{reason}")
        await member.ban(reason=reason)
        await interaction.response.send_message(f"Banned {member}\nReason:{reason}")

    # Exeption in case if the member doen't have the permissions
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You Don't Have The Permissions To Ban !")

# Setup
def setup(client):
    client.add_cog(Ban(client))
