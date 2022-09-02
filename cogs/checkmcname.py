import nextcord, sys
from nextcord.ext import commands
sys.path.insert(1, 'cogs\lib')
import values as v

guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")

class CheckMcName(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(guild_ids=guilds, description="Check Wether A Minecraft Name Is Availble Or Not")
    async def checkmcname(self, interaction: nextcord.Interaction, name: str = nextcord.SlashOption(description="The Name You Want To Check")):
        mcEmbed = nextcord.Embed(
            title=f"{name}",
            description=f"Click The Text Above To Check If The Username Is Availble Or Not",
            url=f"https://namemc.com/search?q={name}",
            color=embedColor,
        )
        await interaction.response.defer()
        await interaction.followup.send(embed=mcEmbed)

# Setup
def setup(client):
    client.add_cog(CheckMcName(client))
