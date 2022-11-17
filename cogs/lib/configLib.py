import json

class Config():
    def __init__(self, guild_id, guild_name):
        self.guild_id = guild_id
        self.guild_name = guild_name

        data = {
            f"server_{self.guild_id}":{
                "guild_id": guild_id,
                "guild_name": str(guild_name)
                "welcome_enabled": False
            }
        }

        with open("config/servers.json", "w") as conf:
            json.dump(data, conf)

#Getter methods
    def get_server_name(self, guild_id):
        with open("config/servers.json", "r") as conf:
            data = json.load(conf)
        
        server_name = data["server"]["guild_id"]
        return server_name
    
    def get_welcome_status(self, guild_id):
        with open("config/servers.json", "r") as conf:
            data = json.load(conf)
        
        welcome_status = data[f"server_{guild_id}"]["welcome_enabled"]
        return welcome_status

#Setter methods
    def set_welcome_status(self, guild_id, status):
        data = {
            f"server_{guild_id}":{
                "guild_id": guild_id,
                "guild_name": str(guild_name)
                "welcome_enabled": status
            }
        }
        with open("config/servers.json", "r") as conf:
            json.dump(data, conf)