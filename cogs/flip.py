import nextcord, sys
from nextcord.ext import commands
import random
sys.path.insert(1, 'cogs\lib')
import values as v

guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")

class flipcoin(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(guild_ids=guilds, description="Flips a coin", force_global = True)
    async def flipcoin(self, interaction: nextcord.Interaction):
            choices = ["heads","tails"]
            random.shuffle(choices)
            final_choice = random.choice(choices)

            await interaction.response.defer()
            await interaction.followup.send(f"<@{interaction.user.id}> {final_choice}")
# Setup
def setup(client):
    client.add_cog(flipcoin(client))