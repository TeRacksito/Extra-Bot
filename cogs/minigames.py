"""
minigames cog module

Implements `MiniGames cog class`.
"""

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from cooldowns import define_shared_cooldown, shared_cooldown, SlashBucket, CallableOnCooldown

from cogs.lib.values import DataFetcher as DF
from cogs.lib.minesweeper_generator import generate_map

guilds= DF.get("guilds")
embeds = DF.get("embeds")
minesweeper_embed = embeds["minesweeper"]

class MiniGames(commands.Cog):
    """
    MiniGames cog class
    
    Implements simple retro and arcade like games with slash commands.
    """
    define_shared_cooldown(2, 8, SlashBucket.author, cooldown_id="MiniGames_cooldown")

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command()
    async def minigames(self, interaction: Interaction):
        """
        minigames slash command category.
        """

    @minigames.subcommand(description= "A configurable MineSweeper minigame!")
    @shared_cooldown("MiniGames_cooldown")
    async def minesweeper(self, interaction: Interaction,
                          difficulty: float = SlashOption(default= float(5.0), max_value= float(10.0), min_value= float(0.0),
                                                        description= "The difficulty of the game. From 0 - 10!"),
                          height: int = SlashOption(default= 4, max_value= 8, min_value= 2,
                                                    description= "The height of the grid table."),
                          width: int = SlashOption(default= 6, max_value= 12, min_value= 2,
                                                   description= "The width of the grid table.")):
        """
        minesweeper slash subcommand

        Generates a minesweeper game within given parameters.

        All the parameters given have a recommended maximum values, but the generator function could
        handle more than that in case is needed. Read generator function docstring for more info.

        Parameters
        ----------
        difficulty : `float, optional`
            An inverse factor that determines the number of mines based on the size of the grid.
            The higher "difficulty" is, the more mines there will be. Allowed values from 0 to 10, by default 5.

        height : `int, optional`
            The number of rows the grid will have. Allowed values from 2 to 8, by default 4.
        width : `int, optional`
            The number of columns the grid will have. Allowed values from 2 to 12, by default 6.
        """
        await interaction.response.defer()

        try:
            minesweeper = generate_map("discord_paste, mines, metadata", height, width, difficulty)
        except ValueError:
            await interaction.send("Not allowed values!", ephemeral= True)
        except RecursionError:
            await interaction.send("We couldn't generate the MineSweeper map due to **excessive number of mines**.\n"+
                                   "However, this could solve itself if you **try again!**")

        embed = nextcord.Embed()
        embed.set_thumbnail(minesweeper_embed["thumbnail_url"])
        embed.color = minesweeper_embed["color"]
        embed.title = minesweeper_embed["title"]
        if minesweeper["mines"] > 1:
            s_pointer = "s"
        else:
            s_pointer = ""
        
        if minesweeper["metadata"]:
            solution_pointer = "Has at least one possible solution!"
        else:
            solution_pointer = "There may not be a possible solution..."
        embed.set_footer(text= f"{height}x{width} grid with {minesweeper['mines']} mine{s_pointer}.\n"+
                         f"{solution_pointer}",
                         icon_url= minesweeper_embed["thumbnail_url"])

        embed.description = minesweeper["discord_paste"]
        await interaction.send(embed= embed)

    @minesweeper.error
    async def on_cooldown(self, interaction: Interaction, error: nextcord.ApplicationError):
        """
        on_cooldown function

        Generic on cooldown handler.
        """
        if isinstance(error, CallableOnCooldown):
            await interaction.send(ephemeral= True,
                                   content= f"You are being rate-limited! Retry in `{round(error.retry_after, 2)}` seconds.")
# Setup
def setup(bot: commands.Bot):
    # pylint: disable=missing-function-docstring
    bot.add_cog(MiniGames(bot))
