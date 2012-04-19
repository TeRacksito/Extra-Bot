import nextcord
from nextcord.ext import commands
from random import choice, shuffle
from configparser import ConfigParser

config=ConfigParser()
config.read(".\config.ini")
guild_id_1=config["options"]["guild1_id"]
guild_id_2=config["options"]["guild2_id"]
guilds=[int(guild_id_1),int(guild_id_2)]

class YesOrNo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(guild_ids=guilds, description="Yes Or No Command Ask the bot a question")
    async def yesorno(self, interaction: nextcord.Interaction, question: str = nextcord.SlashOption(description="Question", required=True)):
        answers = ["Yes", "No", "Of Course", "Of Course ||No||", "I Can't Decide","是的，但是中文","不"]
        shuffle(answers)
        Embed = nextcord.Embed(title=question, description=f"{choice(answers)}", color=0x2852fa)
        await interaction.response.send_message(embed=Embed)

# Setup
def setup(client):
    client.add_cog(YesOrNo(client))
