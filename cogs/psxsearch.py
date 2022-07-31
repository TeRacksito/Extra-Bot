from discord import Embed
import nextcord
from nextcord.ext import commands

class psxsearch(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context = True)
    async def psxsearch(self, ctx, arg1):
        psxEmbed = nextcord.Embed(
            title=arg1,
            description=f"Click The Text Above To Go To Your PSX Search \n\nRequested By <@{ctx.author.id}>",
            url=f"https://petsimulatorvalues.com/search?q={arg1}",
            color=0x2852fa,
        )
        await ctx.send(embed=psxEmbed)

    @psxsearch.error
    async def psxsearch_error(self, ctx, error):
        if isinstance(error , commands.MissingRequiredArgument):
            await ctx.send(f"<@{ctx.author.id}> \nThis Command Usage Is ` -PsxSearch [Pet] `")

#Setup
def setup(client):
    client.add_cog(psxsearch(client))