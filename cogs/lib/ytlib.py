import requests
import values as v

key = v.values.getData("yt_api_key")

class YoutubeLib():
    def GetVideoUrl(Qeury):
        link = f"https://youtube.googleapis.com/youtube/v3/search?key={key}&q={Qeury}&type=video&part=snippet&maxResults=1"
        ytData = requests.get(link).json()
        videoId = ytData["items"][0]["id"]["videoId"]
        videoLink=f"https://www.youtube.com/watch?v={videoId}"
        
        return videoLink
    def GetVideoData(Qeury):
        link = f"https://youtube.googleapis.com/youtube/v3/search?key={key}&q={Qeury}&type=video&part=snippet&maxResults=1"
        ytData = requests.get(link).json()
        
        videoThumb = ytData["items"][0]["snippet"]["thumbnails"]["medium"]["url"]
        videoTitle = ytData["items"][0]["snippet"]["title"]
        videoChannelName = ytData["items"][0]["snippet"]["channelTitle"]
        
        packedData = (videoThumb, videoTitle, videoChannelName)
        
        return packedData
    def GetChannelSubs(channel):
        link = f"https://youtube.googleapis.com/youtube/v3/search?key={key}&q={Qeury}&type=video&part=snippet&maxResults=1"
        ytData = requests.get(link).json()
            