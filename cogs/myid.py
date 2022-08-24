from nextcord import Interaction
import nextcord
from nextcord.ext import commands
from configparser import ConfigParser
from sys import platform

config=ConfigParser()
if platform == "linux" or platform == "linux2":
    config.read("../config.ini")
elif platform == "win32":
    config.read(".\config.ini")
 
guild_id_1=config["options"]["guild1_id"]
guild_id_2=config["options"]["guild2_id"]
guilds=[int(guild_id_1),int(guild_id_2)]

class MyID(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Tell you your discord id useful in some cases

    @nextcord.slash_command(guild_ids=guilds, description="Tell You Your Id In Discord")
    async def myid(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send(f"{interaction.user.id} Is Your Id")


# Setup
def setup(client):
    client.add_cog(MyID(client))
