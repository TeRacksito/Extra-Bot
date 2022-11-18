import nextcord, sys
from nextcord.ext import commands
sys.path.insert(1, 'cogs\lib')
import values as v

guilds=v.values.getData("guilds")
embedColor=v.values.getData("color")
prefix=v.values.getData("prefix")

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Help command
    @nextcord.slash_command(guild_ids=guilds, description="Help Command")
    async def help(self, interaction: nextcord.Interaction):
        help_text = """
        ```
Category:      
    Moderation:           
        /kick [member] - Kicks the specified member            
        /ban - Bans the specified member
                       
    Misc:           
        /myid - Send You Your Discord ID           
        /getid [member] - Get Some Data About the specified member           
        /help - Display this message           
        /clear [Number] - clears the specified number of messages           
        /yesorno [question] - Ask the bot a question      

    Math:
        /add [Number 1] [Number 2] - Adds 2 numbers
        /subtract [Number 1] [Number 2] - Subtracts 2 numbers
        /divide [Number 1] [Number 2] - Divides 2 numbers
        /multiply [Number 1] [Number 2] - Multiplies 2 numbers

    Randomisation:
        /flipcoin - flips a coin, self-explanatory
        /randomnumber [a][b] - Generates a random number between point a and b
        ```
        """
        await interaction.response.defer()
        await interaction.followup.send(help_text)


# setup
def setup(client):
    client.add_cog(Help(client))
