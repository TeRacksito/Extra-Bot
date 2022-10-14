import asyncio
import nextcord
import youtube_dl
import sys
sys.path.insert(1, 'cogs\lib')
from ytlib import YoutubeLib
import values as v 
from nextcord.ext import commands

guilds = v.values.getData("guilds")
class Music(commands.Cog):
    @nextcord.slash_command(guild_ids=guilds)
    async def play(self, interaction: nextcord.Interaction, qeury: str = nextcord.SlashOption(required=True)):
        yt_dl_options = {"format": "bestaudio/best"}
        ffmpeg_options = {"options": "-vn"}

        ytdl = youtube_dl.YoutubeDL(yt_dl_options)

        if interaction.user.voice:
            url = YoutubeLib.GetVideoUrl(Qeury=qeury)

            vc_client1 = await interaction.user.voice.channel.connect()
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = nextcord.FFmpegPCMAudio(song, **ffmpeg_options)
            vc_client1.play(player)
            await interaction.response.defer()
            await interaction.followup.send(f"Now Playing The Requested Song By <@{interaction.user.id}>")

        else:
            await interaction.response.defer()
            await interaction.followup.send("You Are Not In A Voice Channel To Use This Command")

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        if ctx.author.voice:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.reply("The Bot/You Is Not In A Voice Channel To Stop !")


# setup
def setup(client):
    client.add_cog(Music(client))
