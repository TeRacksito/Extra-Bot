import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions
from configparser import ConfigParser
from sys import platform

config=ConfigParser()
if platform == "linux" or platform == "linux2":
    config.read("../config.ini")
elif platform == "win32":
    config.read(".\config.ini")
 
guild_id_1=config["options"]["guild1_id"]
guild_id_2=config["options"]["guild2_id"]
guilds=[int(guild_id_1),int(guild_id_2)]
class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Kick command
    @nextcord.slash_command(guild_ids=guilds, description="Kick The Specified Member")
    @has_permissions(kick_members=True)
    async def kick(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason: str = nextcord.SlashOption(description="The Reason You Want To Kick The Member", required=True)):
        await member.send(f"You Got Kick From The Server \nReason:{reason}")
        await member.kick(reason=reason)
        await interaction.response.defer()
        await interaction.followup.send(f"Kicked {member}\nReason:{reason}")

    # Exeption in case if the member doen't have the permissions
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You Don't Have The Permissions To Kick !")
            
# Setup
def setup(client):
    client.add_cog(Kick(client))
