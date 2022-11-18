import nextcord, sys
from nextcord.ext import commands
sys.path.insert(1, 'cogs\lib')
import values as v
import time

guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")

class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @nextcord.slash_command(guild_ids=guilds, description="Clears a number of messages specified", force_global = True)
    async def clear(self, interaction: nextcord.Interaction, number: int = nextcord.SlashOption(description="Number Of Messages You Want To Delete", required=True)):
            await interaction.channel.purge(limit=number, bulk=True)
            await interaction.response.defer()
            msg = await interaction.followup.send(f"```Sucessfully deleted {number} messages```")
            time.sleep(3)
            await msg.delete()
# Setup
def setup(client):
    client.add_cog(Clear(client))