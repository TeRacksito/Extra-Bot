from nextcord import Interaction
import nextcord, sys
from nextcord.ext import commands
sys.path.insert(1, 'cogs\lib')
import values as v

guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")

class MyID(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Tell you your discord id useful in some cases

    

# Setup
def setup(client):
    client.add_cog(MyID(client))
