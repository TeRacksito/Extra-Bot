import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions


class ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    # ban command
    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.reply(f"Banned {member}\nReason:{reason}")
        await member.send(f"You Got Ban From The Server \nReason:{reason}")

    # Exeption in case if the member doen't have the permissions
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You Don't Have The Permissions To Ban !")

    # ban Command Exception
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"<@{ctx.author.id}> \nThis Command Usage Is ` -ban [member] [reason] `")


# Setup
def setup(client):
    client.add_cog(ban(client))
