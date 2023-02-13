import os
from quart import Quart, render_template, redirect, url_for
from quart-discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from nextcord.ext import ipc
import nextcord
from cogs.lib.values import values

v=values()
app = Quart(__name__)
app.secret_key = "my"

os.environ("OAUTHLIB_INSECURE_TRANSPORT") = "true"

try:
    app.config["DISCORD_CLIENT_ID"] = int(v.getData("client_id"))
    app.config["DISCORD_CLIENT_SECRET"] = intv.getData("secret")
    app.config["DISCORD_CLIENT_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
    app.config["DISCORD_BOT_TOKEN"] = v.getData("token")
    dis = DiscordOAuth2Session(app)
    
    @app.route("/login")
    async def login():
        return await dis.create_session()
    
    @app.route("/callback")
    async def callback():
        try:
            await dis.callback()
        except:
            return redirect(url_for("login"))
        return redirect(url_for("dashboard"))
    
    @app.route("/")
    async def mainPage():
        return await render_template("index/index.html")

    @app.route("/dash")
    async def dash():
        user = await dis.fetch_user()
        return render_template("dash/dashboard.html", user=user)
except:
    def do_nothing():
        #This does nothing bc i have no idea what i should do to "do nothing"
        return

if __name__ == "__main__":
    port=2010
    app.run(debug=True, port=port)
    print(f"Dashboard started @ localhost:{port}")