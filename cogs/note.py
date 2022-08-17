import nextcord
from nextcord.ext import commands


class Note(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Talk to the console
    @commands.command(pass_context=True)
    async def Note(self, ctx, arg):
        if ctx.author.id == 893102684855496724 or 835071335398244355:
            print(arg)
        else:
            await ctx.author.send("You Don't Have Permission To Send Messages To The Console !")


# setup
def setup(client):
    client.add_cog(Note(client))
