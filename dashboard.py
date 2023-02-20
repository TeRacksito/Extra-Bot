import os
from quart import Quart, render_template, redirect, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from nextcord.ext import ipc
import nextcord
from cogs.lib.values import values

v=values()
app = Quart(__name__)
app.secret_key = "my"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

secret=values.getData("secret")
app.config["DISCORD_CLIENT_SECRET"] = secret
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_CLIENT_ID"] = int(values.getData("client_id"))
app.config["DISCORD_BOT_TOKEN"] = values.getData("token")
dis = DiscordOAuth2Session(app)

@app.route("/login")
async def login():
    return await dis.create_session()


@app.route("/")
async def mainPage():
    return await render_template("index/index.html")

@app.route("/dash")
async def dash():
    user = await dis.fetch_user()
    return render_template("dash/dashboard.html", user=user)

@app.route("/callback")
async def callback():
    try:
        await dis.callback()
    except:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    port=2010
    app.run(port=port, debug=True)
# from quart import Quart
# app = Quart(__name__)

# @app.route("/")
# def index():
#     return "hey"
# app.run(port=2010)