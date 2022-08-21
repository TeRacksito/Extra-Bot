import asyncio
from code import interact
import nextcord
import youtube_dl
from nextcord.ext import commands
from configparser import ConfigParser
import time

config=ConfigParser()
config.read(".\config.ini")
guild_id_1=config["options"]["guild1_id"]
guild_id_2=config["options"]["guild2_id"]
guilds=[int(guild_id_1),int(guild_id_2)]

class Music(commands.Cog):
    @nextcord.slash_command(guild_ids=guilds, description="Play The Audio From The Specified Youtube Video")
    async def play(self, interaction: nextcord.Interaction, url: str = nextcord.SlashOption(description="The Youtube Video Url You Want To Play Audio From", required=True)):
        yt_dl_options = {"format": "bestaudio/best"}
        ffmpeg_options = {"options": "-vn"}

        ytdl = youtube_dl.YoutubeDL(yt_dl_options)

        if interaction.user.voice:
            vc_client1 = await interaction.user.voice.channel.connect()
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']  
            player = nextcord.FFmpegPCMAudio(song, **ffmpeg_options)
            vc_client1.play(player)
            print("waiting 1 second")
            time.sleep(1)
            print("done")
            await interaction.response.defer()
            await interaction.followup.send("Play The Requested Song")
        else:
            await interaction.response.defer()
            await interaction.followup.send("You Are Not In A Voice Channel To Use This Command")

    @nextcord.slash_command(guild_ids=guilds, description="Stop The Audio Playing In The Current Channel")
    async def stop(self, interaction: nextcord.Interaction):
        if interaction.user.voice:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.defer()
            await interaction.followup.send(f"Stopped Audio Playing In The Current Voice Channel")
        else:
            await interaction.response.defer()
            await interaction.followup.send("The Bot/You Is Not In A Voice Channel To Stop !")


# setup
def setup(client):
    client.add_cog(Music(client))
