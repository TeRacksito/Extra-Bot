class values():
    def getData(value):
        guild1_id=1009880989318791289
        guild2_id=850066291225133068
        guilds=[guild1_id, guild2_id]
        tokenInConfig=False #Set This To TRUE IF you want to make the token in the config file 
        token=0
        welcome_channel = 1009880989796933754
        embedColor=0x2852fa
        prefix="-"

        #Return The Guild Ids
        if value.lower() == "guilds":
            return guilds
        elif value.lower() == "color":
            return embedColor
        elif value.lower() == "prefix":
            return prefix
        elif value.lower() == "wlc_chnl":
            return welcome_channel
