import nextcord, sys
from nextcord.ext import commands
sys.path.insert(1, 'cogs\lib')
import values as v
from scramble import gen_scramble


guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")

class cubing(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(guild_ids=guilds, description="Generate a rubik's cube scramble", force_global = True)
    async def gen_scramble(self, interaction: nextcord.Interaction):
            await interaction.response.defer()
            scramble = gen_scramble(20)
            embed = nextcord.Embed(title="Rubik's Cube scramble", color=embedColor, description=f"Here's the generated Scramble\n```{scramble}```")
            await interaction.followup.send(embed=embed)
# Setup
def setup(client):
    client.add_cog(cubing(client))