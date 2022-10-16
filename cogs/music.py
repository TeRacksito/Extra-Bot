import asyncio
import nextcord
import youtube_dl
import sys
sys.path.insert(1, 'cogs\lib')
from ytlib import YoutubeLib
import values as v 
from nextcord.ext import commands

guilds = v.values.getData("guilds")
embedColor = v.values.getData("color")

last_video_url = None
last_video_query = None

class Music(commands.Cog):
    @nextcord.slash_command(guild_ids=guilds, description="Looks for the specified query on youtube and plays the most relevant result audio")
    async def play(self, interaction: nextcord.Interaction, qeury: str = nextcord.SlashOption(required=True)):
        global last_video_url
        global last_video_query
        
        yt_dl_options = {"format": "bestaudio/best"}
        ffmpeg_options = {"options": "-vn"}

        ytdl = youtube_dl.YoutubeDL(yt_dl_options)

        if interaction.user.voice:
            await interaction.response.defer()
            url = YoutubeLib.GetVideoUrl(Qeury=qeury)

            vc_client1 = await interaction.user.voice.channel.connect()
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = nextcord.FFmpegPCMAudio(song, **ffmpeg_options)
            vc_client1.play(player)

            vidData = YoutubeLib.GetVideoData(Qeury=qeury)
            vidTitle = vidData[1]
            vidThumbUrl = vidData[0]
            vidMaker = vidData[2]

            ytDataEmbed = nextcord.Embed(title=vidTitle, description=vidMaker, url=url, color=embedColor)
            ytDataEmbed.set_thumbnail(vidThumbUrl)

            last_video_url = url
            last_video_query = qeury
        
            await interaction.followup.send(f"Now Playing The Requested Song By <@{interaction.user.id}>", embed=ytDataEmbed)

        else:
            await interaction.response.defer()
            await interaction.followup.send("You Are Not In A Voice Channel To Use This Command")

    @nextcord.slash_command(guild_ids=guilds, description="Stops the audio playing in the current channel")
    async def stop(self, interaction: nextcord.Interaction):
        if interaction.user.voice:
            await interaction.response.defer()
            await interaction.guild.voice_client.disconnect()
            await interaction.followup.send("Disconnected from the voice channel sucessfully.")
        else:
            await interaction.response.send_message("The Bot/You Is Not In A Voice Channel To Stop !")

    @nextcord.slash_command(guild_ids=guilds, description="plays the last played song by the bot")
    async def again(self, interaction: nextcord.Interaction):
        yt_dl_options = {"format": "bestaudio/best"}
        ffmpeg_options = {"options": "-vn"}

        ytdl = youtube_dl.YoutubeDL(yt_dl_options)

        qeury = last_video_query

        if interaction.user.voice:
            await interaction.response.defer()
            url = last_video_url

            vc_client1 = await interaction.user.voice.channel.connect()
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = nextcord.FFmpegPCMAudio(song, **ffmpeg_options)
            vc_client1.play(player)

            vidData = YoutubeLib.GetVideoData(Qeury=qeury)
            vidTitle = vidData[1]
            vidThumbUrl = vidData[0]
            vidMaker = vidData[2]

            ytDataEmbed = nextcord.Embed(title=vidTitle, description=vidMaker, url=url, color=embedColor)
            ytDataEmbed.set_thumbnail(vidThumbUrl)

            await interaction.followup.send(f"Now Playing The Requested Song By <@{interaction.user.id}>", embed=ytDataEmbed)

        else:
                    await interaction.response.defer()
                    await interaction.followup.send("You Are Not In A Voice Channel To Use This Command")

# setup
def setup(client):
    client.add_cog(Music(client))
