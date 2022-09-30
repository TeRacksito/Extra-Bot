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
        await interaction.response.defer()
        await interaction.followup.send(f"```Category:\n     Moderation:\n          /kick [member] - Kicks the specified member \n          /ban - Bans the specified member \n     Misc:\n          /myid - Send You Your Discord ID\n          /getid [member] - Get Some Data About the specified member\n          /help - Display this message\n          /clear [Number] - clears the specified number of messages\n          /yesorno [question] - Ask the bot a question\n     Minecraft:\n          /checkmcname [name] - Checks wether a minecraft name is availble or not               \n/mcprofile [player] - Check the specified minecraft profile (Currently only the getting skin functionality work)\n     Music:\n          {prefix}play [url] - plays the audio of the video youtube of the specified url\n          {prefix}stop - stops the audio playing in the current channel```")


# setup
def setup(client):
    client.add_cog(Help(client))
