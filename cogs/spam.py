import nextcord
from nextcord.ext import commands

class spam(commands.Cog):
    def __init__(self,client):
        self.client = client

    #spam command self-explanatory
    @commands.command(pass_context = True)
    async def spam(self,ctx, arg1 ,arg2):
        print("Starting Spam Sequence")
        number=int(arg2)
        for i in range(number):
            await ctx.send(arg1)
        print("Spam Sequence Ended")

    #Spam command Exception
    @spam.error
    async def spam_error(self,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"<@{ctx.author.id}> \nThe Command Usage Of This Command is ` -spam [message] [number of messages] `")


#Setup 
def setup(client):
    client.add_cog(spam(client))