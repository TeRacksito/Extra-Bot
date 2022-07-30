from click import pass_context
import nextcord
from nextcord.ext import commands

class checkmcname(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def checkmcname(self,ctx, arg1):
        mcEmbed = nextcord.Embed(
        title=f"{arg1}", 
        description=f"Click The Text Above To Check If The Username Is Availble Or Not \n\nRequested By <@{ctx.author.id}>",
        url=f"https://namemc.com/search?q={arg1}",
        color=0x2852fa,
        )
        await ctx.send(embed=mcEmbed)
#Setup
def setup(client):
    client.add_cog(checkmcname(client))