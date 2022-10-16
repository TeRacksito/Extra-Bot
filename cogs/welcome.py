import nextcord, sys
from nextcord.ext import commands
from values import values

sys.path.insert(1, "cogs\lib")


guilds = values.getData("guilds")
embedColor = values.getData("color")
channel_var = values.getData("wlc_chnl")
welcome_message = values.getData("wlc_message")
server_name = values.getData("guild_name")
welcomeServer = values.getData("wlc_enabled_guild")


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild.id

        if guild == welcomeServer:
            channel = self.client.get_channel(channel_var)
            embed = nextcord.Embed(title=f"Hello Welcome To {server_name}", description=welcome_message)
            await member.send(embed=embed)
            await channel.send(f"Welcome To The Server, <@{member.id}>")


# Setup
def setup(client):
    client.add_cog(Welcome(client))
