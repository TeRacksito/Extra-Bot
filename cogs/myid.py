from code import interact
from discord import Interaction
import nextcord
from nextcord.ext import commands
from configparser import ConfigParser

config=ConfigParser()
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
        await interaction.response.send_message(f"{interaction.user.id} Is Your Id")


# Setup
def setup(client):
    client.add_cog(MyID(client))
