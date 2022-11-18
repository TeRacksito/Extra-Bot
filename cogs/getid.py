import nextcord, sys 
from nextcord.ext import commands
sys.path.insert(1, 'cogs\lib')
import values as v

guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")

class GetID(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Get ID Command Self Explanatory
    @nextcord.slash_command(guild_ids=guilds, description="Get The Id Of A Specific Member", force_global = True)
    async def getid(self, interaction: nextcord.Interaction, member: nextcord.Member):
        IdEmbed = nextcord.Embed(
            title=f"{member._user}'s Id",
            color=embedColor,
            description=f"The Id Of {member._user} is {member.id}")
        IdEmbed.set_thumbnail(member.avatar.url)
        IdEmbed.add_field(name="Joined Discord on", value=member.created_at)
        IdEmbed.add_field(name="Joined This Server on", value=member.joined_at)
        await interaction.response.defer()
        await interaction.followup.send(embed=IdEmbed)
        
    @nextcord.slash_command(guild_ids=guilds, description="Tell You Your Id In Discord")
    async def myid(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(f"{interaction.user.id} Is Your Id")
        
# Setup
def setup(client):
    client.add_cog(GetID(client))
