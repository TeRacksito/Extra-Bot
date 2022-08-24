import nextcord
from nextcord.ext import commands
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

class CheckMcName(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(guild_ids=guilds, description="Check Wether A Minecraft Name Is Availble Or Not")
    async def checkmcname(self, interaction: nextcord.Interaction, name: str = nextcord.SlashOption(description="The Name You Want To Check")):
        mcEmbed = nextcord.Embed(
            title=f"{name}",
            description=f"Click The Text Above To Check If The Username Is Availble Or Not",
            url=f"https://namemc.com/search?q={name}",
            color=0x2852fa,
        )
        await interaction.response.defer()
        await interaction.followup.send(embed=mcEmbed)

# Setup
def setup(client):
    client.add_cog(CheckMcName(client))
