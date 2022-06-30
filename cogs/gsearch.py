import nextcord 
from nextcord.ext import commands

class gsearch(commands.Cog):
    def __init__(self, client):
        self.client = client
    #Google Search Command
    @commands.command(pass_context=True)
    async def gSearch(self,ctx, arg):
        await ctx.reply(f"https://www.google.com/search?query={arg}")

    #Google Search Exception
    @gSearch.error
    async def gSearch_error(self,error,ctx):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(f"<@{ctx.autor.id}> \nThe Command Usage Of This Command Is ` -gSearch [Query]")

#Setup
def setup(client):
    client.add_cog(gsearch(client))