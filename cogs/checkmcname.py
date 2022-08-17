import nextcord
from nextcord.ext import commands


class CheckMcName(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def checkmcname(self, ctx, arg1):
        mcEmbed = nextcord.Embed(
            title=f"{arg1}",
            description=f"Click The Text Above To Check If The Username Is Availble Or Not \n\nRequested By <@{ctx.author.id}>",
            url=f"https://namemc.com/search?q={arg1}",
            color=0x2852fa,
        )
        await ctx.send(embed=mcEmbed)

    @checkmcname.error
    async def checkmcname_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"<@{ctx.author.id}> \nThis Command Usage Is ` -CheckMcName [Name] `")


# Setup
def setup(client):
    client.add_cog(CheckMcName(client))
