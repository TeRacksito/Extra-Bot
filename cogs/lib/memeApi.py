import requests
import json

def gen_meme():
        url = "https://meme-api.com/gimme"
        response = json.loads(requests.request("GET", url).text)
        nsfw = response["nsfw"]
        meme = response["preview"][3]
        if nsfw == True:
            return "https://cdn.discordapp.com/attachments/1027493896055439360/1068566682571919421/meme_blocked.png"
        else:
            return meme