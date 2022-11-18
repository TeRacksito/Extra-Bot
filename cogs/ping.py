import nextcord, sys
from nextcord.ext import commands
sys.path.insert(1, 'cogs\lib')
import values as v

guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(guild_ids=guilds, description="Gives you the current ping of the bot", force_global = True)
    async def ping(self, interaction: nextcord.Interaction):
            await interaction.response.defer()
            dataEmbed = nextcord.Embed(title="Pong!", description=f"The bot's ping is {round(self.client.latency * 1000)}ms", color=embedColor)
            await interaction.followup.send(embed=dataEmbed)
# Setup
def setup(client):
    client.add_cog(ping(client))