import nextcord
from nextcord.ext import commands
import os

token=os.getenv('BOTTOKEN')#gets the environment variable that is the bot token i made one

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
client=commands.Bot(command_prefix='-',intents=intents)

#useless code
@client.event
async def on_ready():
    channel1 = client.get_channel(990095039533301820)
    await channel1.send("The bot restarted")
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="This Server"))
    print("The Bot Is Up And Running")
    print("-------------------------")

#Tell you your discord id useful in some cases
@client.command(pass_context=True)#the pass_context = True allows argumentts
async def Myid(ctx):
    await ctx.reply(ctx.author.id)

#Send a link to the bot's page (Not Acessible by anyone exept me)
@client.command()
async def devPortal(ctx):
    await ctx.reply("https://discord.com/developers/applications/865731091125895229/bot")

#spam command self-explanatory
@client.command(pass_context = True)
async def spam(ctx, arg1 ,arg2):
    print("Starting Spam Sequence")
    number=int(arg2)
    fnum=str(number)
    for i in range(number):
        await ctx.send(arg1)
    print("Spam Sequence Ended")

#shutdown command
@client.command()
async def shutdown(ctx):
    #making sure not everone can't shutdown the bot
    if ctx.author.id == 835071335398244355:
        await ctx.reply("Shutting Down The Bot")
        quit()
    else:
        await ctx.reply("You Don't Have The Premisson To Shutdown The Bot !")
    
#Google Search Command
@client.command(pass_context=True)
async def gsearch(ctx, arg):
    await ctx.reply(f"https://www.google.com/search?query={arg}")

#Youtube Search Command
@client.command(pass_context=True)
async def ytvid(ctx, arg):
    await ctx.reply(f"https://www.youtube.com/results?search_query={arg}")    

client.run(token)#runs the bot check the chat btw it has alot of stuff explained