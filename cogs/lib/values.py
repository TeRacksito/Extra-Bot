#Very Baisic Api
import os

import youtube_dl


class values():
    def getData(value):
        guild1_id=1009880989318791289
        guild2_id=850066291225133068
        guild3_id=977477205573652518
        guilds=[guild1_id, guild2_id,guild3_id]

        welcomeEnabledServerID = 977477205573652518
        welcome_channelID = 977477205573652521
        server_name = f"Extra Bot Discord Server"
        welcome_message = f"Welcome This is {server_name} which was made for stuff about the extra bot"

        embedColor=0x2852fa
        prefix="-"

        token = os.getenv("BOTTOKEN")
        youtube_api_key = os.getenv("YTTOKEN")

        if value.lower() == "guilds":
            return guilds
        elif value.lower() == "color":
            return embedColor
        elif value.lower() == "prefix":
            return prefix
        elif value.lower() == "wlc_chnl":
            return welcome_channelID
        elif value.lower() == "guild_name":
            return server_name
        elif value.lower() == "wlc_message":
            return welcome_message
        elif value.lower() == "token":
            return token
        elif value.lower() == "yt_api_key":
            return youtube_api_key
        elif value.lower() == "wlc_enabled_guild":
            return welcomeEnabledServerID