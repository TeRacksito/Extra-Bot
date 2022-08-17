import nextcord
from nextcord.ext import commands


class devportal(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Send a link to the bot's page (Not Acessible by anyone exept me)
    @commands.command()
    async def devPortal(self, ctx):
        await ctx.author.send("https://discord.com/developers/applications/865731091125895229/bot")


# Setup
def setup(client):
    client.add_cog(devportal(client))
