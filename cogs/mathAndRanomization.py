import nextcord, sys
from nextcord.ext import commands
sys.path.insert(1, 'cogs\lib')
import values as v
import random

guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")

class Cog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @nextcord.slash_command(guild_ids=guilds, description="Generates a random number between A and B")
    async def random_number(self, interaction: nextcord.Interaction, a: str = nextcord.SlashOption(required=True), b: str = nextcord.SlashOption(required=True)):
            try:
                num1 = int(a)
                num2 = int(b)
                
                #Generates a random number and stores it in a variable
                random_num = random.randint(num1, num2)
                await interaction.response.defer()
                await interaction.followup.send(f"The random Number Generated Between {a} and {b} is {random_num}")
            except ValueError:
                await interaction.response.defer()
                await interaction.followup.send(f"The provided parameters '{a}' and '{b}' are NOT numbers! \nPlease provide a number to continue")

# Setup
def setup(client):
    client.add_cog(Cog(client))