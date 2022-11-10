#Very Basic Api
import os
import youtube_dl
from configparser import ConfigParser


class values():
    def getData(value):
        guild1_id = 1009880989318791289
        guild2_id = 850066291225133068
        guild3_id = 977477205573652518
        guilds = [guild1_id, guild2_id,guild3_id]

        embedColor=0x2852fa
        prefix="-"

        config = ConfigParser()
        config.read("..\..\options.ini")
        token = config["options"]["bot_token"]
        youtube_api_key = config["options"]["yt_api"]
        
        data = {
            "guilds": guilds,
            "color": embedColor,
            "prefix": prefix,
            "token": token,
            "yt_api_key": youtube_api_key
        }
        
        return data.get(value.lower())
