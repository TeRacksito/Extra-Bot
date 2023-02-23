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

app.config["DISCORD_CLIENT_ID"] = v.getData("client_id")
app.config["DISCORD_CLIENT_SECRET"] = v.getData("secret")
app.config["DISCORD_CLIENT_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = v.getData("token")