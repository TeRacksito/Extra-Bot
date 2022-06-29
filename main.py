from pydoc import Helper
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions, MissingPermissions
import os

token=os.getenv('BOTTOKEN')#gets the environment variable that is the bot token i made one

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
client=commands.Bot(command_prefix='-',intents=intents,help_command=None)

#useful code
@client.event
async def on_ready():
    channel1 = client.get_channel(990095039533301820)
    await channel1.send("The bot restarted")
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="This Server"))
    print("The Bot Is Up And Running")
    print("-------------------------")

#Help command
@client.command()
async def help(ctx):
    embed = nextcord.Embed(title="Commands" ,color=0x2852fa,description="-help - Display This Message \n-kick [Member] [Reason] - Kick A Spesific Member \n-spam [Message] [Number] - Spam A Spesific Message A Number Of Times \n-ytSearch [Query] - Search On Youtube For Query \n-gSearch [Quers] - Search On Google For Query \n-Myid - Tell You Your Id")
    await ctx.reply(embed=embed)

#Talk to the console
@client.command(pass_context=True)
async def Note(ctx,arg):
    if ctx.author.id == 893102684855496724 or 835071335398244355:
        print(arg)
    else:
        await ctx.reply("You Don't Have Permission To Send Messages To The Console !")

#Kick command
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx,member: nextcord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.reply(f"Kicked {member} because {reason}")

#Exeption in case if the member doen't have the permissions
@kick.error
async def kick_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.reply("You Don't Have The Permissions To Kick !")

#Kick Command Exception
@kick.error
async def kick_error(ctx , error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"<@{ctx.author.id}> There is 1 or more missing argument(s) !")

#Tell you your discord id useful in some cases
@client.command(pass_context=True)#the pass_context = True allows argumentt
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
    for i in range(number):
        await ctx.send(arg1)
    print("Spam Sequence Ended")

@spam.error
async def spam_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"<@{ctx.author.id}> There is 1 missing argument !")

#shutdown command
@client.command()
async def shutdown(ctx):
    #making sure not everone can't shutdown the bot
    if ctx.author.id == 835071335398244355 or 893102684855496724:
        await ctx.reply("Shutting Down The Bot")
        quit()
    else:
        await ctx.reply("You Don't Have The Premisson To Shutdown The Bot !")
    
#Google Search Command
@client.command(pass_context=True)
async def gSearch(ctx, arg):
    await ctx.reply(f"https://www.google.com/search?query={arg}")

#Google Search Exception
@gSearch.error
async def gSearch_error(error,ctx):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(f"<@{ctx.autor.id}> There is 1 missing argument !")

#Youtube Search Command
@client.command(pass_context=True)
async def ytSearch(ctx, arg):
    await ctx.reply(f"https://www.youtube.com/results?search_query={arg}")    

#Youtube Search Exception
@ytSearch.error
async def ytSearch_error(error,ctx):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(f"<@{ctx.author.id}> There is 1 missing argument !")

client.run(token)#runs the bot 