import nextcord
from nextcord.ext import commands
from nextcord import Interaction

class help(commands.Cog):
    def __init__(self,client):
        self.client = client
        
    #Help command
    @commands.command()
    async def help(self, ctx):
        embed = nextcord.Embed(
        title="Commands",
        color=0x2852fa,
        description=f"-help - Display This Message \n-kick [Member] [Reason] - Kick A Spesific Member \n-spam [Message] [Number] - Spam A Spesific Message A Number Of Times \n-ytSearch [Query] - Search On Youtube For Query \n-gSearch [Quers] - Search On Google For Query \n-Myid - Tell You Your Id \n-Lyrics [Artist] [Song] - Search For A Song's Lyrics By Artist \n-YesOrNo [Question] - Ask The Bot A Question \n-CheckMcName [Name] - Check If A Minecraft Name Is Avaible Or Not  \n \n Requested By <@{ctx.author.id}>")
        await ctx.send(embed=embed)

#setup
def setup(client):
    client.add_cog(help(client))
