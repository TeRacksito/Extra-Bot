import nextcord 
from nextcord.ext import commands
from random import choice , shuffle

class yesorno(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(pass_context=True)
    async def yesorno(self, ctx , arg1):
        answers = ["Yes", "No", "Of Course", "Of Course No", "I Can't Decide"]
        shuffle(answers)
        Embed = nextcord.Embed(title=arg1, description=f"{choice(answers)} \n \n Requested By <@{ctx.author.id}>", color=0x2852fa)
        await ctx.send(embed=Embed)
	
    @yesorno.error
    async def yesorno_error(self, ctx , error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"<@{ctx.author.id}> \nThe Command Usage Of This Command is ` -yesOrNo [Question] `")
#Setup
def setup(client):
    client.add_cog(yesorno(client))
