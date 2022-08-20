import nextcord
from nextcord.ext import commands
from configparser import ConfigParser

config=ConfigParser()
config.read(".\config.ini")
guild_id_1=config["options"]["guild1_id"]
guild_id_2=config["options"]["guild2_id"]
guilds=[int(guild_id_1),int(guild_id_2)]


class GetID(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Get ID Command Self Explanatory
    @nextcord.slash_command(guild_ids=guilds, description="Get The Id Of A Specific Member")
    async def getid(self, interaction: nextcord.Interaction, member: nextcord.Member):
        IdEmbed = nextcord.Embed(
            title=f"{member._user}'s Id",
            color=0x2852fa,
            description=f"The Id Of {member._user} is {member.id}")
        IdEmbed.set_thumbnail(member.avatar.url)
        await interaction.response.defer()
        await interaction.followup.send(embed=IdEmbed)

# Setup
def setup(client):
    client.add_cog(GetID(client))
