#Very Basic Api
import os
import youtube_dl
import tomli

class values():
    def getData(value):
        guild1_id = 1009880989318791289
        guild2_id = 850066291225133068
        guild3_id = 977477205573652518
        guilds = [guild1_id, guild2_id,guild3_id]

        embedColor=0x2852fa
        prefix="-"

        #Configuration system ???
        with open("config.toml", mode = "rb") as fp:
            config = tomli.load(fp)
        token = config["options"]["bot_token"]
        
        if not token:
            tkn = config["options"]["bot_token_env"]
            token = os.getenv("tkn")
        
        data = {
            "guilds": guilds,
            "color": embedColor,
            "prefix": prefix,
            "token": token
        }
        
        return data.get(value.lower())
