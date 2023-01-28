import nextcord, sys
from nextcord.ext import commands
sys.path.insert(1, 'cogs\lib')
import values as v
from memeApi import gen_meme

guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")

class meme(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @nextcord.slash_command(guild_ids=guilds, description="Generates an SFW meme and sends it to the chat, this command sometimes works and sometimes not", force_global = True, dm_permission = True)
    async def meme(self, interaction: nextcord.Interaction):
            await interaction.response.defer()
            meme = gen_meme()
            meme_embed = nextcord.Embed(title="Here's a meme", color=embedColor)
            meme_embed.set_image(url = meme)
            meme_embed.set_footer(text="Powered by meme api on Github ==> https://github.com/D3vd/Meme_Api", icon_url="https://cdn.discordapp.com/attachments/1027493896055439360/1068564499763830804/GitHub-Mark.png")
            await interaction.followup.send(embed=meme_embed)
        
# Setup
def setup(client):
    client.add_cog(meme(client))