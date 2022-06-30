from lyricsgenius import Genius
import nextcord
from nextcord.ext import commands
import os
class lyrics(commands.Cog):
    def __init__(self,client):
        self.client = client

    #lyrics command
    @commands.command(pass_context=True)
    async def lyrics(self,ctx,artist,song):
        token=open("Z:\\discord bot (GITHUB)\\ghast-town-bot\\ghast-town-bot\\cogs\\genuisApiKey.txt","r")
        genius = Genius(token.read())
        artist = genius.search_artist(artist,max_songs=1)
        song = artist.song(song)
        
        embed = nextcord.Embed(title=song.title + " by " + song.artist, description=song.lyrics, color=0x2852fa)
        await ctx.reply(embed=embed)

    #lyrics command exception
    @lyrics.error
    async def lyrics_error(self,ctx,error):
        if isinstance(error, commands.MissingRequiredArgument):
            ctx.send(f"<@ctx.author.id> This Command Usage Is \n-lyrics [Artist Name] [Song]")



#Setup 
def setup(client):
    client.add_cog(lyrics(client))