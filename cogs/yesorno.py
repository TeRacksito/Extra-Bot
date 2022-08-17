import nextcord
from nextcord.ext import commands
from random import choice, shuffle


class YesOrNo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(guild_ids=[977477205573652518], description="Youtube Search Command")
    async def yesorno(self, interaction: nextcord.Interaction, question: str = nextcord.SlashOption(description="Question", required=True)):
        answers = ["Yes", "No", "Of Course", "Of Course No", "I Can't Decide"]
        shuffle(answers)
        Embed = nextcord.Embed(title=question, description=f"{choice(answers)}", color=0x2852fa)
        await interaction.response.send_message(embed=Embed)

# Setup
def setup(client):
    client.add_cog(YesOrNo(client))
