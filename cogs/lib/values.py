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

        welcomeEnabledServerID = 977477205573652518
        welcome_channelID = 977477205573652521
        server_name = f"Extra Bot Discord Server"
        welcome_message = f"Welcome This is {server_name} which was made for stuff about the extra bot"

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
            "wlc_chnl": welcome_channelID,
            "guild_name": server_name,
            "wlc_message": welcome_message,
            "token": token,
            "yt_api_key": youtube_api_key,
            "wlc_enabled_guild": welcomeEnabledServerID
        }
        
        return data.get(value.lower())
