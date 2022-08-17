import nextcord
from nextcord.ext import commands


class myid(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Tell you your discord id useful in some cases

    @commands.command(pass_context=True)  # the pass_context = True allows argumentt
    async def Myid(self, ctx):
        await ctx.reply(ctx.author.id)


# Setup
def setup(client):
    client.add_cog(myid(client))
