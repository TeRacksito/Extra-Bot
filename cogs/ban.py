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

class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ban command
    @nextcord.slash_command(guild_ids=guilds, description="Ban Sepcified Member")
    @has_permissions(ban_members=True)
    async def ban(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason: str = nextcord.SlashOption(description="The Reason You Want To Ban The Member", required=True)):
        await member.send(f"You Got Ban From The Server \nReason:{reason}")
        await member.ban(reason=reason)
        await interaction.response.defer()
        await interaction.followup.send(f"Banned {member}\nReason:{reason}")

# Setup
def setup(client):
    client.add_cog(Ban(client))
