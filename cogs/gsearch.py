import nextcord
from nextcord.ext import commands


class gsearch(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Google Search Command
    @commands.command(pass_context=True)
    async def gSearch(self, ctx, arg):
        gEmbed = nextcord.Embed(
            title=arg,
            description=f"Click The Text Above To Go To Your Google Search \n\nRequested By <@{ctx.author.id}>",
            url=f"https://www.google.com/search?query={arg}",
            color=0x2852fa,
        )
        gEmbed.set_thumbnail("https://cdn.discordapp.com/attachments/991958269012758548/1003379889069641758/google.png")
        await ctx.send(embed=gEmbed)

    # Google Search Exception
    @gSearch.error
    async def gSearch_error(self, error, ctx):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"<@{ctx.autor.id}> \nThe Command Usage Of This Command Is ` -gSearch [Query]")


# Setup
def setup(client):
    client.add_cog(gsearch(client))
