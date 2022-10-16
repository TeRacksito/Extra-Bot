import nextcord, sys
from nextcord.ext import commands
from mojang import MojangAPI
from values import values

sys.path.insert(1, 'cogs\lib')


guilds = values.getData("guilds")
embedColor = values.getData("color")
channel = values.getData("wlc_chnl")

async def follow_up(interaction, content):
    await interaction.response.defer()
    if isinstance(content, str):
        await interaction.followup.send(content)
    else:
        await interaction.followup.send(embed=content)
        

class Minecraft(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command
    @nextcord.slash_command(guild_ids=guilds, description="Check If A Minecraft Name Is Availble Or Not")
    async def checkmcname(self, interaction:nextcord.Interaction, name: str = nextcord.SlashOption(description="The Name Of The Minecraft Player You Want To Check", required=True)):
        player = MojangAPI.get_uuid(name)

        content = None
        if not player:
            content = nextcord.Embed(title=name, description=f"The Minecraft Name {name} Is Availabe", color=embedColor)
        elif " " in name:
            content = "The Requested Name Contains an invalid character"
        else:
            content = nextcord.Embed(title=name, description=f"The Minecraft Name {name} Is Unvailabe", color=embedColor)
           
        await follow_up(interaction, content)

    @nextcord.slash_command(guild_ids=guilds, description="View the profile of the specified minecraft player")
    async def mcprofile(self, interaction: nextcord.Interaction, name: str = nextcord.SlashOption(description="The minecraft player you want to see his profile")):
        player = MojangAPI.get_uuid(name)
        
        if not player:
            content = "This minecraft player doesn't exist."
        else:
            content = nextcord.Embed(color=embedColor, description="Click the title to get the player's skin", title=name, url=profile.skin_url)
            
        await follow_up(interaction, content)

# Setup
def setup(client):
    client.add_cog(Minecraft(client))
