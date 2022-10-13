import asyncio
import nextcord
import youtube_dl
import sys
sys.path.insert(1, 'cogs\lib')
from ytlib import YoutubeLib
from nextcord.ext import commands

class Music(commands.Cog):
    @commands.command(pass_context=True)
    async def play(self, ctx, qeury):
        yt_dl_options = {"format": "bestaudio/best"}
        ffmpeg_options = {"options": "-vn"}

        ytdl = youtube_dl.YoutubeDL(yt_dl_options)

        if ctx.author.voice:
            url = YoutubeLib.GetVideoUrl(Qeury=qeury)

            vc_client1 = await ctx.author.voice.channel.connect()
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = nextcord.FFmpegPCMAudio(song, **ffmpeg_options)
            vc_client1.play(player)
            await ctx.reply(f"Now Playing The Requested Song By <@{ctx.author.id}>")

        else:
            await ctx.reply("You Are Not In A Voice Channel To Use This Command")

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        if ctx.author.voice:
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.reply("The Bot/You Is Not In A Voice Channel To Stop !")


# setup
def setup(client):
    client.add_cog(Music(client))
