import nextcord
from nextcord.ext import commands
from nextcord.ext.commands import has_permissions


class Unban(commands.Cog):
    def __init__(self, client):
        self.client = client

    # unban command
    @commands.command()
    @has_permissions(ban_members=True)
    async def unban(self, ctx, member: nextcord.Member):
        await member.unban()
        await ctx.reply(f"Unbanned {member}")
        await member.send(f"You Got UNBan From The Server")

    # Exeption in case if the member doen't have the permissions
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("You Don't Have The Permissions To unban !")

    # unban Command Exception
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"<@{ctx.author.id}> \nThis Command Usage Is ` -unban [member] `")


# Setup
def setup(client):
    client.add_cog(Unban(client))
