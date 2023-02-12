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
    
    @nextcord.slash_command(guild_ids=guilds, description="Generates a random number between A and B", force_global = True)
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

    @nextcord.slash_command(guild_ids=guilds, description="Adds 2 numbers if you are too lazy to use your brain", force_global = True)
    async def add(self, interaction: nextcord.Interaction, number_1: str = nextcord.SlashOption(required=True), number_2: str = nextcord.SlashOption(required=True)):
            try:
                num1 = int(number_1)
                num2 = int(number_2)
                sum = num1 + num2

                await interaction.response.defer()
                await interaction.followup.send(f"{num1} + {num2} is {sum}")
            except ValueError:
                await interaction.response.defer()
                await interaction.followup.send(f"The provided parameters '{number_1}' and '{number_2}' are NOT numbers! \nPlease provide a number to continue")

    @nextcord.slash_command(guild_ids=guilds, description="Subtracts 2 numbers if you are too lazy to use your brain", force_global = True)
    async def subtract(self, interaction: nextcord.Interaction, number_1: str = nextcord.SlashOption(required=True), number_2: str = nextcord.SlashOption(required=True)):
            try:
                num1 = int(number_1)
                num2 = int(number_2)
                sum = num1 - num2

                await interaction.response.defer()
                await interaction.followup.send(f"{num1} - {num2} is {sum}")
            except ValueError:
                await interaction.response.defer()
                await interaction.followup.send(f"The provided parameters '{number_1}' and '{number_2}' are NOT numbers! \nPlease provide a number to continue")

    @nextcord.slash_command(guild_ids=guilds, description="Divides 2 numbers if you are too lazy to use your brain", force_global = True)
    async def divide(self, interaction: nextcord.Interaction, number_1: str = nextcord.SlashOption(required=True), number_2: str = nextcord.SlashOption(required=True)):
            try:
                num1 = int(number_1)
                num2 = int(number_2)
                sum = num1 / num2

                await interaction.response.defer()
                await interaction.followup.send(f"{num1} / {num2} is {sum}")
            except ValueError:
                await interaction.response.defer()
                await interaction.followup.send(f"The provided parameters '{number_1}' and '{number_2}' are NOT numbers! \nPlease provide a number to continue")
            except ZeroDivisionError:
                await interaction.response.send_message("Cannot Divide by zero")

    @nextcord.slash_command(guild_ids=guilds, description="Multiplies 2 numbers if you are too lazy to use your brain", force_global = True)
    async def multiply(self, interaction: nextcord.Interaction, number_1: str = nextcord.SlashOption(required=True), number_2: str = nextcord.SlashOption(required=True)):
            try:
                num1 = int(number_1)
                num2 = int(number_2)
                sum = num1 * num2

                await interaction.response.defer()
                await interaction.followup.send(f"{num1} * {num2} is {sum}")
            except ValueError:
                await interaction.response.defer()
                await interaction.followup.send(f"The provided parameters '{number_1}' and '{number_2}' are NOT numbers! \nPlease provide a number to continue")

# Setup
def setup(client):
    client.add_cog(Cog(client))