import requests
import values as v

class YoutubeLib():
    def GetVideoUrl(Qeury):
        key = v.values.getData("yt_api_key")
        link = f"https://youtube.googleapis.com/youtube/v3/search?key={key}&q={Qeury}&type=video&part=snippet&maxResults=1"
        ytData = requests.get(link).json()
        videoId = ytData["items"][0]["id"]["videoId"]
        videoLink=f"https://www.youtube.com/watch?v={videoId}"
        
        return videoLink
