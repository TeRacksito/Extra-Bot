import nextcord
from nextcord.ext import commands


class Shutdown(commands.Cog):
    def __init__(self, client):
        self.client = client

    # shutdown command
    @commands.command()
    async def shutdown(self, ctx):
        # making sure not everone can't shutdown the bot
        if ctx.author.id == 835071335398244355 or 893102684855496724:
            await ctx.author.send("Shutting Down The Bot")
            quit()
        else:
            await ctx.author.send("You Don't Have The Premisson To Shutdown The Bot !")


# Setup
def setup(client):
    client.add_cog(Shutdown(client))
