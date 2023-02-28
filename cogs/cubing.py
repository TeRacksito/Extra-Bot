import nextcord, sys
from nextcord.ext import commands
sys.path.insert(1, 'cogs\lib')
import values as v
from pyTwistyScrambler import scrambler333


guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")

class cubing(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(guild_ids=guilds, description="Generate a rubik's cube scramble using the Official WCA format", force_global = True)
    async def gen_scramble(self, interaction: nextcord.Interaction):
            await interaction.response.defer()
            scramble = scrambler333.get_WCA_scramble()
            embed = nextcord.Embed(title="Rubik's Cube scramble", color=embedColor, description=f"Here's the generated Scramble\n```{scramble}```")
            await interaction.followup.send(embed=embed)
    
    @nextcord.slash_command(guild_ids=guilds, description="Generates a scramble for the last layer, useful for training OLL", force_global = True)
    async def last_layer_scramble(self, interaction: nextcord.Interaction):
            await interaction.response.defer()
            scramble = scrambler333.get_LL_scramble()
            embed = nextcord.Embed(title="Last Layer scramble", color=embedColor, description=f"Here's the generated Last Layer Scramble\n```{scramble}```")
            await interaction.followup.send(embed=embed)
    
    @nextcord.slash_command(guild_ids=guilds, description="Generates a scramble that has the cross only solved, usefull for training F2L", force_global = True)
    async def f2l_scramble(self, interaction: nextcord.Interaction):
            await interaction.response.defer()
            scramble = scrambler333.get_LL_scramble()
            embed = nextcord.Embed(title="Cross solved only scramble", color=embedColor, description=f"Here's the generated Scramble\n```{scramble}```")
            await interaction.followup.send(embed=embed)
    
# Setup
def setup(client):
    client.add_cog(cubing(client))