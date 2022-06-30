import nextcord 
from nextcord.ext import commands

class ytsearch(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Youtube Search Command
    @commands.command(pass_context=True)
    async def ytSearch(self,ctx, arg):
        await ctx.reply(f"https://www.youtube.com/results?search_query={arg}")    

    #Youtube Search Exception
    @ytSearch.error
    async def ytSearch_error(self,error,ctx):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send(f"<@{ctx.author.id}> \nThe Command Usage Of This Command Is ` -ytSearch [Query]")

#Setup 
def setup(client):
    client.add_cog(ytsearch(client))