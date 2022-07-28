import nextcord
from nextcord.ext import commands
import os

token=os.getenv('BOTTOKEN')#gets the environment variable that is the bot token i made one

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
client=commands.Bot(command_prefix='-',intents=intents,help_command=None, case_insensitive=True)

#useful code
@client.event
async def on_ready():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="This Server"))
    print("The Bot Is Up And Running")
    print("-------------------------")

#Cogs
innitial_extensions = []

for i in os.listdir(".\cogs"):
    if i.endswith(".py"):
        innitial_extensions.append("cogs." + i[:-3])

if __name__ == "__main__":
    for extension in innitial_extensions:
        client.load_extension(extension)


client.run(token)#runs the bot