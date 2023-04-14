"""
math_and_randomization cog module

Implements `Maths cog class`.
"""
import random

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from cooldowns import define_shared_cooldown, shared_cooldown, SlashBucket, CallableOnCooldown

from cogs.lib.values import DataFetcher as DF

guilds= DF.get("guilds")

class EmptyRangeError(ValueError):
    """
    EmptyRangeError custom ValueError exception

    A custom exception intended to be raised when a given set of
    numbers are the same.
    """
    def __init__(self, message, *args):
        self.message = message
        super(EmptyRangeError, self).__init__(message, *args)

class Maths(commands.Cog):
    """
    Maths cog class

    Implements slash commands for basic math operations and randomization.
    """
    define_shared_cooldown(2, 8, SlashBucket.author, cooldown_id="Maths_cooldown")

    def __init__(self, bot):
        self.bot = bot

    def format_numbers(self, number_a: str, number_b: str, is_range: bool = False) -> float | int:
        """
        format_numbers function

        Format the given strings representations of floats or integers.
        Attempts to convert the strings to floats type. If the floats are
        integers, then convert them to integers type, depends on is_range value.

        Parameters
        ----------
        number_a : `str`
            A string representation of float or integer. Otherwise, a
            `ValueError` exception is raised.
        number_b : `str`
            A string representation of float or integer. Otherwise, a
            `ValueError` exception is raised.
        is_range : `bool, optional`
            If the numbers are attempting to conform a range, by default False.

        Returns
        -------
        `float | int`
            The numbers converted to float or integer objects.

        Raises
        ------
        `ValueError`
            If at least one string does not represent float nor integer.
        
        `EmptyRangeError`
            A custom ValueError exception. If the given numbers are the same.
            No range can be conformed between.
        """

        # If the strings do not represent a float, ValueError is raised.
        number_a: float = float(number_a)
        number_b: float = float(number_b)

        # If the numbers are attempting to conform a range...
        if is_range:

            # [a, b] range always must be a < b.
            if number_a > number_b:
                number_a, number_b = number_b, number_a

            # Python ranges [a, b] allow a == b.
            # But only one number exists in such a range,
            # so always random number will be the same.
            elif number_a == number_b:
                raise EmptyRangeError("The given numbers are the same. No range between can be conformed.")

            # If both floats could be integer objects...
            if number_a.is_integer() and number_b.is_integer():
                number_a = int(number_a)
                number_b = int(number_b)

        else:
            # If any float could be integer object...
            if number_a.is_integer():
                number_a = int(number_a)
            if number_b.is_integer():
                number_b = int(number_b)

        return number_a, number_b

    def not_number_error(self, number_a: str | float, number_b: str | float) -> str:
        """
        not_number_error function

        Handles the generic not number error that happens along all
        slash commands of this class.

        Parameters
        ----------
        number_a : `str | float`
            If it is a string, then it cannot represent a float | integer.
        number_b : `str | float`
            If it is a string, then it cannot represent a float | integer.

        Returns
        -------
        `str`
            The correct error message to be send to the user in function on
            what number parameters are string objects.
        """
        try:
            number_a = float(number_a)
        except ValueError:
            pass
        try:
            number_b = float(number_b)
        except ValueError:
            pass

        # If both numbers are not float nor integer...
        if isinstance(number_a, str) and isinstance(number_b, str):
            return f"The provided parameters *number_a* (`{number_a}`) and *number_b* (`{number_b}`) are NOT numbers!"
        # If a is not float nor integer...
        elif isinstance(number_a, str):
            return f"The provided parameter *number_a* (`{number_a}`) is NOT number!"
        # If b is not float nor integer...
        else:
            return f"The provided parameter *number_b* (`{number_b}`) is NOT number!"

    def scientific_notation(self, num: float | int) -> float | int:
        """
        scientific_notation function

        Formats the number to scientific notation if needed.

        When the number is too small, then is formatted to
        scientific notation. If not, round to four decimals is
        attempted, but only applied if needed. The number could
        be returned without any changes.

        Parameters
        ----------
        num : `float | int`
            The number to be formatted, rounded or returned without
            changes.

        Returns
        -------
        'float | int'
            A number on scientific notation or rounded, could be just
            an integer object.
        """
        # If the absolute value of the number is smaller than...
        if abs(num) < 0.0001:
            # pylint: disable=consider-using-f-string
            # Apply scientific notation using built-in format function.
            return "{:.3e}".format(num)
        else:
            try:
                # If the float could be integer object.
                if (num).is_integer():
                    num = int((num))
            except AttributeError:
                # The number is already integer object.
                pass
            return round(num, 4)

    @nextcord.slash_command(guild_ids= guilds, force_global= True,
                            description= "Generates a random number between A and B, including both end points")
    @shared_cooldown("Maths_cooldown")
    async def random_number(self, interaction: Interaction,
                            number_a: str = SlashOption(required= True,
                                                        description= "A number, 2 for example."),
                            number_b: str = SlashOption(required= True,
                                                        description= "A number, 5 for example.")):
        """
        random_number slash command

        Generates a random number between two given numbers, including both end points.

        Parameters
        ----------
        number_a : `str`
            A string representation of float | integer.
        number_b : `str`
            A string representation of float | integer.
        """
        await interaction.response.defer()
        try:
            number_a, number_b = self.format_numbers(number_a, number_b, is_range= True)
            if isinstance(number_a, int) and isinstance(number_b, int):
                # Generates a random integer and stores it in a variable.
                random_num = random.randint(number_a, number_b)
            else:
                # Generates a random float and stores it in a variable.
                random_num = round(random.uniform(number_a, number_b), 3)
            await interaction.followup.send(f"The random number generated between `{number_a}` and `{number_b}` is `{random_num}`")
        except EmptyRangeError:
            # If the numbers are equals among themselves...
            await interaction.followup.send(f"The numbers are the same (`{number_a}`), so no random number can be chosen.")
        except ValueError:
            # If at least one number is not a number...
            not_number = self.not_number_error(number_a, number_b)
            await interaction.followup.send(f"{not_number}\n"+
                                            "Please provide a number parameter next time.")
            del not_number

    @nextcord.slash_command(guild_ids= guilds, force_global= True,
                            description= "Adds 2 numbers if you are too lazy to use your brain.")
    @shared_cooldown("Maths_cooldown")
    async def add(self, interaction: Interaction,
                  number_a: str = SlashOption(required= True,
                                              description= "A number, 4 for example."),
                  number_b: str = SlashOption(required= True,
                                              description= "A number, -8 for example.")):
        """
        add slash command

        Calculates the sum of two given numbers.

        Parameters
        ----------
        number_a : `str`
            A string representation of float | integer.
        number_b : `str`
            A string representation of float | integer.
        """
        await interaction.response.defer()
        try:
            number_a, number_b = self.format_numbers(number_a, number_b)
            output = self.scientific_notation(number_a + number_b)
            await interaction.followup.send(f"`{number_a} + {number_b}` is `{output}`")
        except ValueError:
            # If any of the strings does not represent float nor integer.
            not_number = self.not_number_error(number_a, number_b)
            await interaction.followup.send(f"{not_number}\n"+
                                            "Please provide a number parameter next time.")
            del not_number

    @nextcord.slash_command(guild_ids= guilds, force_global= True,
                            description= "Subtracts 2 numbers if you are too lazy to use your brain.")
    @shared_cooldown("Maths_cooldown")
    async def subtract(self, interaction: Interaction,
                       number_a: str = SlashOption(required= True,
                                                   description= "A number, -2 for example."),
                       number_b: str = SlashOption(required= True,
                                                   description= "A number, 7 for example.")):
        """
        subtract slash command

        Calculates the rest of two given numbers.

        Parameters
        ----------
        number_a : `str`
            A string representation of a float | integer.
        number_b : `str`
            A string representation of a float | integer.
        """
        await interaction.response.defer()
        try:
            number_a, number_b = self.format_numbers(number_a, number_b)
            output = self.scientific_notation(number_a - number_b)
            await interaction.followup.send(f"`{number_a} - {number_b}` is `{output}`")
        except ValueError:
            # If any of the strings does not represent float nor integer.
            not_number = self.not_number_error(number_a, number_b)
            await interaction.followup.send(f"{not_number}\n"+
                                            "Please provide a number parameter next time.")
            del not_number

    @nextcord.slash_command(guild_ids= guilds, force_global= True,
                            description= "Divides 2 numbers if you are too lazy to use your brain.")
    @shared_cooldown("Maths_cooldown")
    async def divide(self, interaction: Interaction,
                     number_a: str = SlashOption(required= True,
                                                 description= "A number as a dividend, 8 for example."),
                     number_b: str = SlashOption(required= True,
                                                 description= "A number as a divisor, 3 for example. Cannot be 0.")):
        """
        divide slash command

        Calculates the division of two given numbers. Returns the value
        rounded up to two decimals.

        Parameters
        ----------
        number_a : `str`
            A string representation of a float | integer dividend.
        number_b : `str`
            A string representation of a float | integer divisor.
        """
        await interaction.response.defer()
        try:
            number_a, number_b = self.format_numbers(number_a, number_b)
            try:
                output = self.scientific_notation(number_a / number_b)
                await interaction.followup.send(f"`{number_a} / {number_b}` is `{output}`")
            except ZeroDivisionError:
                await interaction.followup.send(f"`{number_a} / {number_b}`, cannot divide by zero.")
        except ValueError:
            # If any of the strings does not represent float nor integer.
            not_number = self.not_number_error(number_a, number_b)
            await interaction.followup.send(f"{not_number}\n"+
                                            "Please provide a number parameter next time.")
            del not_number

    @nextcord.slash_command(guild_ids= guilds, force_global = True,
                            description= "Multiplies 2 numbers if you are too lazy to use your brain.")
    @shared_cooldown("Maths_cooldown")
    async def multiply(self, interaction: Interaction,
                       number_a: str = SlashOption(required= True,
                                                   description= "A number, 5 for example."),
                       number_b: str = SlashOption(required= True,
                                                   description= "A number, 20 for example.")):
        """
        multiply slash command

        Calculates the multiplication of two given numbers.

        Parameters
        ----------
        number_a : `str`
            A string representation of a float | integer multiplicand.
        number_b : `str`
            A string representation of a float | integer multiplier.
        """
        await interaction.response.defer()
        try:
            number_a, number_b = self.format_numbers(number_a, number_b)
            output = self.scientific_notation(number_a * number_b)
            await interaction.followup.send(f"`{number_a} · {number_b}` is `{output}`")
        except ValueError:
            # If any of the strings does not represent float nor integer.
            not_number = self.not_number_error(number_a, number_b)
            await interaction.followup.send(f"{not_number}\n"+
                                            "Please provide a number parameter next time.")
            del not_number

    @random_number.error
    @add.error
    @subtract.error
    @divide.error
    @multiply.error
    async def on_cooldown(self, interaction: Interaction, error: nextcord.ApplicationError):
        """
        on_cooldown function

        Generic on cooldown handler.
        """
        if isinstance(error, CallableOnCooldown):
            await interaction.send(ephemeral= True,
                                   content= f"You are being rate-limited! Retry in `{round(error.retry_after, 2)}` seconds.")
# Setup
def setup(bot):
    # pylint: disable=missing-function-docstring
    bot.add_cog(Maths(bot))
