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
app.config["DISCORD_REDIRECT_URI"] = "https://ahmed3457-scaling-enigma-gwjj5rp5j753v5gw-5000.githubpreview.dev/callback"
app.config["DISCORD_CLIENT_ID"] = int(values.getData("client_id"))
app.config["DISCORD_BOT_TOKEN"] = values.getData("token")
ipc = ipc.Client(secret_key="my")
dis = DiscordOAuth2Session(app)

@app.route("/login")
async def login():
    return await dis.create_session()


@app.route("/")
async def mainPage():
    return await render_template("index/index.html")

@app.route("/dashboard")
async def dash():
    user = await dis.fetch_user()
    return await render_template("dash/dashboard.html", user=user)

@app.route("/callback")
async def callback():
    try:
        await dis.callback()
    except:
        return redirect(url_for("login"))
    return redirect(url_for("dash"))

if __name__ == "__main__":
    port=5000
    app.run(port=port, debug=True)