import nextcord
import os, sys
from nextcord.ext import commands
sys.path.insert(1, 'cogs/lib')
import values as v

prefix=v.values.getData("prefix")
configData=v.values.getData("tokendetails")

token = os.getenv('BOTTOKEN')

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix=prefix, intents=intents, help_command=None, case_insensitive=True)


# useful code
@client.event
async def on_ready():
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="/help"))
    print("---------------------------------------------------------------")
    print("___________         __                  __________        __   \n\_   _____/__  ____/  |_____________    \______   \ _____/  |_ \n |    __)_\  \/  /\   __\_  __ \__  \    |    |  _//  _ \   __|\n |        \>    <  |  |  |  | \// __ \_  |    |   (  <_> )  |  \n/_______  /__/\_ \ |__|  |__|  (____  /  |______  /\____/|__|  \n        \/      \/                  \/          \/             ")
    print("---------------------------------------------------------------")


# Cogs
innitial_extensions = []

for i in os.listdir("cogs"):
    if i.endswith(".py"):
        innitial_extensions.append("cogs." + i[:-3])

if __name__ == "__main__":
    for extension in innitial_extensions:
        client.load_extension(extension)

client.run(token)  # runs the bot
