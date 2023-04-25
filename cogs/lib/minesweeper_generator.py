"""
minesweeper_generator module

Implements a minesweeper map generator with custom algorithm and some tools.

Raises
------
`ValueError`
    If any height or width are lower than 2.

`ValueError`
    If no parts were given or the given ones are unknown. Also the parts have to be given as
    string, string representation of a list or list of strings.

`RecursionError`
    If `max_fails` limit is reached. Generally, this means that there are too many mines to be placed.
"""
import copy
import datetime
import random
import sys
# pylint: disable=too-many-lines
from pprint import pprint

import numpy

from cogs.lib.terminal import SGR

# Discord emojis binding to matrix possible values.
discord_emoji_table = {
    -1: ":bomb:",
    0: ":white_large_square:",
    1: ":one:",
    2: ":two:",
    3: ":three:",
    4: ":four:",
    5: ":five:",
    6: ":six:",
    7: ":seven:",
    8: ":eight:",
}

# set List of allowed payload parts.
allowed_parts = set(
    [
        "matrix",
        "decorated_matrix",
        "discord_paste",
        "mines",
        "metadata",
    ]
)

def generate_map(parts: str | list,
                 height: int,
                 width: int,
                 difficulty: int,
                 max_fails: int = 500,
                 debug_level: int = 0,
                 final_report: bool = False) -> dict:
    """
    generate_map function

    Generates a MineSweeper map within given parameters using a custom algorithm.

    This generator has implemented some debugging and anti-hung tools to make computationally
    secure generations and easily modifiable algorithms.

    If the docstring of this algorithm is not enough to understand it, then you can read this
    post that describes this exact algorithm. -- https://stackoverflow.com/a/76086333/14012058

    Algorithm
    ---------

        This algorithm `checks if` the generated map `has at least one possible solution`,
        but only for grids with an area of 10000 cells or lower. Anyway, it also checks a series
        of conditions for each mine placed using recursive methods.

        For each mine to be placed, the steps below are followed:

        - First, a `cell is randomly chosen` considering the entire grid. Fails and tries again if the cell is not empty.

        - Second, the `range of all contiguous cells` to the chosen cell is computed. Then each contiguous cell
        is iterated and checked. `Two main conditions` are checked, the number of surrounding `valid empty cells` and
        if every surrounding `mine is still valid` if the current one was placed. If one of the conditions fails,
        then the cell is discarded as invalid and failed attempts counter increases by one.

        - A `valid empty cell` is one that is surrounded by at least `four empty cells`. Note that, due to recursive 
        limit, the surrounding empty cells to the empty cell being checked are not also checked. This means that the
        surrounding empty cells to the empty cell being checked could not have at least four surrounding empty cells.

        - A `valid mine` is one that has at least three surrounding `valid empty cells`. Note that, when three surrounding
        valid empty cells are already found while checking a mine, then no more empty cells will be checked,
        but mines will continue to be searched to validate.

        - When a `mine` is found while checking the surrounding cells, then that mine will be checked recursively having as a
        parent the mine before it. If another mine is found, then again it will be checked recursively having as parents the mines
        before it. This recursive search will stop if more than four mine cells are found straight, reaching the concatenated mine limit.
        Then the main parent cell that is being checked will be discarded as invalid for new mines.

        - Finally, if all surrounding mines and those surrounding them are valid and the concatenated mine limit was not reached,
        the current checked cell will be set as a mine.

        - This process will stop in two cases. First, if no more mines have to be placed and all mines have been placed
        correctly. Second, if the failed attempts counter reaches a certain limit, by default 500. The failed attempts limit
        should be set larger if large grids with higher proportions of mines are computed.

    Parameters
    ----------
    parts : `str | list`
        The parts to being returned in the payload.

        - `matrix`: return the computed matrix as a list of lists.
        - `decorated_matrix`: return a decorated version of the matrix using SGR format. Useful for print reasons.
        - `discord_paste`: return a string that represents the version of the matrix formatted to be sended on a
        discord message. This is the playable part of the MineSweeper generator.
        - `mines`: Return the number of mines in the current MineSweeper game.
        - `metadata`: Return additional data. Like failed attempts number and if the generated map has a verified solution.

    height : `int`
        The number of rows the grid will have. This value should never be smaller than 2. The computational effort
        increases exponentially with this value as a factor.

    width : `int`
        The number of columns the grid will have. This value should never be smaller than 2. The computational effort
        increases exponentially with this value as a factor.

    difficulty : `int`
        An inverse factor that determines the number of mines based on the size of the grid.
        The higher "difficulty" is, the more mines there will be. This value should never be larger than 12.
        The computational effort increases exponentially as difficulty aproches 12 or any larger. Approximations to 12
        could end in `RecursionError` if `max_fails` is too small or even with high values.

    max_fails : `int, optional`
        The maximum number of failed attempts of placing a cell, by default `500`.

    debug_level : `int, optional`
        The debugging level of the generator as an integer, by default `0`.

        - `level 1` announces in terminal when a mine placement will be performed, where in the
        grid will be done, and the result of the attempt.

        - `level 2` does the same that previos levels. But also prints every step done on every attempt.
        This is useful to understand what is happening within the algorithm and the result of literally
        every single step done. Warning: this will cause terminal spamming, that increases exponentially
        with the size of the grid and the number of mines as factors.
    
    final_report : `bool`
        In case you want the final report with the decorated matrix but not the other debugging messages,
        by default `False`.

    Returns
    -------
    `dict`
        The payload as a result of the generation. The keys of the dict are the parts asked for.

    Raises
    ------
    `ValueError`
        If any `height` or `width` are lower than 2.

    `ValueError`
        If no `parts` were given or the given ones are unknown. Also the `parts` have to be given as
        string, string representation of a list or list of strings.

    `RecursionError`
        If `max_fails` limit is reached. Generally, this means that there are too many mines to be placed.
    """
    if height < 2 or width < 2:
        raise ValueError(height, width, "Grid too small!")

    if isinstance(parts, str):
        parts_list = [part.strip().lower() for part in parts.split(",")]

        if not parts_list:
            raise ValueError(parts, "No parts were given!")
    elif isinstance(parts, list):
        parts_list = parts

    else:
        raise ValueError(parts, "Parts must be string or list")

    not_allowed_parts = list(set(parts_list) - allowed_parts)

    if not_allowed_parts:
        raise ValueError(parts, f"Unknown parts: {not_allowed_parts}")

    del not_allowed_parts

    mines = int((height * width)//(15 - difficulty))

    # Internal function definition. Not defined outside to preserve local bounds and internal purposes.
    def check_empty(_matrix: list, object_x: int, object_y:int , _level: int) -> bool:
        """
        check_empty function

        Internal checking function. Should never be called outside `generate_map` function.

        Checks if surroundings of given empty cell have at least three empty cells.

        Parameters
        ----------
        _matrix : `list`
            The list of lists representation of matrix structure.

        object_x : `int`
            Cell x position. Represent the column index.

        object_y : `int`
            Cell y position. Represent the row index.

        _level : `int`
            The current recursion level.

        Returns
        -------
        `bool`
            If the given empty cell is valid or not.
        """
        if debug_level > 1:
            # Debugging purposes.
            placement_row = copy.deepcopy(_matrix[object_y])
            placement_row[object_x] = str(placement_row[object_x]) + SGR.format("?", SGR.Foreground.yellow)
            print(f"{'|   '*_level}checking empty x{object_x} y{object_y} -> ", end= "")
            _string = "["
            for _cell in placement_row:
                _cell = str(_cell)
                if len(_cell) == 1:
                    _cell = f" {SGR.format(_cell, SGR.Foreground.rgb(100, 100, 100))} "
                else:
                    if "?" in _cell or "!" in _cell:
                        if "-1" not in _cell:
                            _cell = f" {_cell}"
                    else:
                        _cell = f"{SGR.format(_cell, SGR.Foreground.red)} "
                _string += f"{_cell}"
            _string += "]\n"
            print(_string, end= "")

        # Computes the surrounding range of the given cell.
        top_x = object_x
        top_y = object_y
        bottom_x = object_x
        bottom_y = object_y

        if object_x >= 1:
            top_x -= 1

        if object_y >= 1:
            top_y -= 1

        if object_x <= width-2:
            bottom_x += 1

        if object_y <= height -2:
            bottom_y += 1

        # Conditions counter that must be met.
        _conditions = {"empty": 0}
        for _y in range(top_y, bottom_y +1):
            for _x in range(top_x, bottom_x +1):
                if _x == object_x and _y == object_y:
                    continue

                # Value of the surrounding _X, _y cell.
                _value = _matrix[_y][_x]

                # If the surrounding cell is empty...
                if _value == 0:
                    _conditions["empty"] += 1

            # Every row checking if conditions are already met.
            if _conditions["empty"] >= 4:
                if debug_level > 1:
                    # Debugging purposes.
                    print(f"{'|   '*_level}" + SGR.format(f"{'+' * _level}Good!", SGR.Foreground.green))
                return True

        # If conditions are never met...
        if debug_level > 1:
            # Debugging purposes.
            print(f"{'|   '*_level}" + SGR.format(f"{'-'*_level}Bad! ({_conditions})", SGR.Foreground.red))
        return False

    def check_mine(_matrix: list, object_x: int, object_y: int, _level: int, _parents: list):
        """
        check_mine internal function

        Internal checking function. Should never be called outside `generate_map` function.

        Checks if given mine cell still valid if parents changes were applied.

        Parameters
        ----------
        _matrix : `list`
            The list of lists representation of matrix structure.

        object_x : `int`
            Cell x position. Represent the column index.

        object_y : `int`
            Cell y position. Represent the row index.

        _level : `int`
            The current recursion level.

        _parents : `list`
            The list of dict representation of parents coordinates.

        Returns
        -------
        `bool`
            If the given mine cell is valid or not.
        """
        if debug_level > 1:
            # Debugging purposes.
            print(f"{'|   '*_level}checking mine x{object_x} y{object_y}")
            placement_matrix = copy.deepcopy(_matrix)
            placement_matrix[object_y][object_x] = str(placement_matrix[object_y][object_x]) + SGR.format("?", SGR.Foreground.green)
            for _parent in _parents:
                placement_matrix[_parent["y"]][_parent["x"]] = (str(placement_matrix[_parent["y"]][_parent["x"]]) +
                                                                SGR.format("!", SGR.Foreground.magenta))
            _string = str()
            # pylint: disable=consider-using-enumerate
            for _row_index in range(len(placement_matrix)):
                _string += f"{'|   '*_level}["
                for _column_index in range(len(placement_matrix[_row_index])):
                    _value = str(placement_matrix[_row_index][_column_index])
                    if len(_value) == 1:
                        _value = f" {SGR.format(_value, SGR.Foreground.rgb(100, 100, 100))} "
                    else:
                        if "?" in _value or "!" in _value:
                            if "-1" not in _value:
                                _value = f" {_value}"
                        else:
                            _value = f"{SGR.format(_value, SGR.Foreground.red)} "
                    _string += f"{_value}"
                _string += "]\n"
            print(_string)

        # Computes the surrounding range of the given cell.
        top_x = object_x
        top_y = object_y
        bottom_x = object_x
        bottom_y = object_y

        if object_x >= 1:
            top_x -= 1

        if object_y >= 1:
            top_y -= 1

        if object_x <= width-2:
            bottom_x += 1

        if object_y <= height -2:
            bottom_y += 1

        # Conditions counter that must be met.
        _conditions = {"empty": 0, "mines": 0}
        if _level < 3:
            additional_error_info = str()
            for _y in range(top_y, bottom_y +1):
                for _x in range(top_x, bottom_x +1):
                    # If the coordinates _x & _y are the given cell itself...
                    if _x == object_x and _y == object_y:
                        continue

                    is_parent = False
                    # Check if coordinates _x & _y are parents.
                    for _parent in _parents:
                        if _x == _parent["x"] and _y == _parent["y"]:
                            if debug_level > 1:
                                # Debugging purposes.
                                print(f"{'|   '*_level}x{_x} y{_y} is parent! -> {_parents}")
                            is_parent = True
                    if is_parent:
                        continue

                    # Value of the cell.
                    _value = _matrix[_y][_x]

                    # If cell contains a mine...
                    if _value == -1:
                        parents.append({"x": object_x, "y": object_y})
                        # Check recursively if the mine still valid.
                        if check_mine(_matrix, _x, _y, _level +1, copy.deepcopy(parents)):
                            _conditions["mines"] += 1
                        else:
                            # Bad condition.
                            _conditions["mines"] = 100
                            break

                    # If the cell is empty and the condition for empty cells has not yet been met...
                    if _value == 0 and _conditions["empty"] < 3:
                        if check_empty(_matrix, _x, _y, _level +1):
                            _conditions["empty"] += 1
                        else:
                            continue

                # Useful statement that breaks recursion if some bad conditions are met
                # and therefore no longer matters what happens later.
                if _conditions["empty"] < 0 or _conditions["mines"] > 2 or _conditions["mines"] < 0:
                    break

            # If conditions are met...
            if _conditions["empty"] >= 3 and _conditions["mines"] <= 2:
                if debug_level > 1:
                    # Debugging purposes.
                    print(f"{'|   '*_level}" + SGR.format(f"{'+' * _level}Good!", SGR.Foreground.green))
                return True
        # If mine concatenation limit is reached...
        else:
            additional_error_info = "Mine concatenation limit!"
        # If conditions are never met...
        if debug_level > 1:
            # Debug purposes.
            print(f"{'|   '*_level}" + SGR.format(f"{'-'*_level}Bad! {additional_error_info} ({_conditions})", SGR.Foreground.red))
        return False

    def grid_generator(height: int, width: int):
        """
        grid_generator internal function

        Generates a grid with given parameters. Also generates a copy
        of that grid, but each element is has a dict of its coordinates
        instead of the element's value itself.

        Parameters
        ----------
        height : `int`
            The number of rows the grid will have.
        width : `int`
            The number of columns the grid will have. 

        Returns
        -------
        list, list
            Return two matrix.
        """
        # Generation of empty matrix with given parameters.
        matrix = list()
        matrix_register = list()
        for row_index in range(height):
            row = list()
            row_register = list()
            for cell_index in range(width):
                row.append(0)
                row_register.append({"x": cell_index, "y": row_index})
            matrix.append(row)
            matrix_register.append(row_register)

        return matrix, matrix_register

    def solver(matrix: list, debug_level: int):
        """
        solver algorithm

        This function will attempt to solve the generated minesweeper map.

        First, a `logical simplifier` is used, useful for most cases. Second, `matrix operations`
        are done to discover if there are more complex moves to be done. Note that matrix operations
        will perform `predictions` in the most complex cases, if predictions go wrong, then the generated
        map is discarded as no possible solution map.

        Also, if the generated map does not have any `0/empty cell`, then also will be discarded as no possible
        solution map. `0/empty cell` is one that does not have any bomb surrounding it.

        Parameters
        ----------
        matrix : `list`
            The generated minesweeper map represented as a matrix, which in turn, is a representation of a list of lists.
        debug_level : `int`
            The debug level for the solver. It works equals to the parent generator map algorithm.
        """
        def print_hidden(hidden_matrix: list):
            """
            print_hidden internat function

            Prints the hidden matrix with complex indentation. Useful to be able to visualize 
            nicely the matrix, almost like a game board.

            Parameters
            ----------
            hidden_matrix : `list`
                The matrix to be printed, this could be also the original matrix.
            """
            # The string where the matrix will be formatted in.
            string = str()
            for hidden_row_index, hidden_row in enumerate(hidden_matrix):
                # Note how spaces are left to create a perfect grid perception, depending on the size
                # of the value.
                string += f"{SGR.format('[', SGR.Foreground.rgb(100, 100, 100))} "
                for hidden_column_index, hidden_cell in enumerate(hidden_row):
                    if hidden_cell is None:
                        # Computes the surrounding range of the chosen cell.
                        top_left_x = hidden_column_index
                        top_left_y = hidden_row_index
                        bottom_right_x = hidden_column_index
                        bottom_right_y = hidden_row_index

                        if hidden_column_index >= 1:
                            top_left_x -= 1

                        if hidden_row_index >= 1:
                            top_left_y -= 1

                        if hidden_column_index <= width -2:
                            bottom_right_x += 1

                        if hidden_row_index <= height -2:
                            bottom_right_y += 1

                        # Counting variables.
                        important = False
                        stop = False
                        # pylint: disable=invalid-name
                        for y in range(top_left_y, bottom_right_y +1):
                            for x in range(top_left_x, bottom_right_x +1):
                                # If the coordinates x & y are the chosen cell itself...
                                if x == hidden_column_index and y == hidden_row_index:
                                    continue

                                value = hidden_matrix[y][x]

                                if value is not None:
                                    important = True
                                    stop = True
                                    break
                            if stop:
                                break
                        if important:
                            string += "None "
                        else:
                            string += f"{SGR.format('None', SGR.Foreground.rgb(100, 100, 100))} "

                    elif hidden_cell == -1:
                        string += f" {SGR.format('-1', SGR.Foreground.red)}  "
                    elif hidden_cell != 0 and isinstance(hidden_cell, int):
                        string += f"  {SGR.format(hidden_cell, SGR.Foreground.rgb(255, 200 - (25 * hidden_cell), 0))}  "
                    elif hidden_cell != 0:
                        string += f"  {SGR.format(hidden_cell, SGR.Foreground.green)}  "
                    else:
                        string += f"  {SGR.format(hidden_cell, SGR.Foreground.rgb(100, 100, 100))}  "
                string += f"{SGR.format(']', SGR.Foreground.rgb(100, 100, 100))}\n"
            print(string)

        def solve_simple(matrix: list, hidden_matrix: list):
            """
            solve_simple internal function

            Works as an initiator of the solver loop.

            Parameters
            ----------
            matrix : `list`
                The generated minesweeper map represented as a matrix, which in turn, is a representation of a list of lists.
            hidden_matrix : `list`
                A copy of `matrix` but with hidden values. This represents the state of the game. Works as normal game.
            """
            def simplifier(matrix: list, co_hidden_matrix: list):
                """
                simplifier internat function

                Uses logical operations to simplify the current state of the generated map.

                Works great for most cases.

                Parameters
                ----------
                matrix : `list`
                    The generated minesweeper map represented as a matrix, which in turn, is a representation of a list of lists.
                co_hidden_matrix : `list`
                    A copy of `matrix` but with hidden values. This represents the state of the game. Works as normal game.

                Returns
                -------
                solved `bool`
                    If the generated map was solved while it was being simplified.

                hidden_matrix `list`
                    A copy of `matrix` but with hidden values. This represents the state of the game. Works as normal game.
                    Includes the changes done during the simplification.

                total_objects `list`
                    All cells (every cell is a tuple like `(x, y)`) that are active and important in the current state of `hidden_matrix`.
                    This refers to all hidden cells that are surrounded by non 0/empty revealed cells.

                matrix_equation_variables `list`
                    The matrix with the `equations` of each non 0/empty revealed cells. Note that those cells that refers to the same hidden
                    cells are removed, that means that duplicates are removed.

                matrix_equation_equals `list`
                    The matrix with the values of each `equation` within `matrix_equation_variables`.
                    If `matrix_equation_variables` and `matrix_equation_equals` were appended together, they
                    would form an `augmented matrix`.
                
                Raises
                ------
                `ValueError`
                    If an unexpected value was found while iterating `hidden_matrix`.
                """
                # Counting variables.
                simplified = False
                simplification_attempts = 0
                # Initialize the simplify loop.
                while not simplified and simplification_attempts < 300:
                    simplification_attempts += 1
                    if debug_level > 1:
                        print_hidden(matrix)
                        print_hidden(co_hidden_matrix)

                    # Get all equation for each non 0/empty revealed cells and only if they are surrounded by at least one
                    # hidden cell.
                    equations = set()
                    all_nones = 0
                    all_found_mines = 0
                    for hidden_row_index, hidden_row in enumerate(co_hidden_matrix):
                        for hidden_column_index, hidden_cell in enumerate(hidden_row):
                            # If hidden_cell is not empty nor mine and does not still hidden.
                            if hidden_cell not in [0, None, "b"]:
                                # If the cell was revealed and is a mine. Game over.
                                # This is normally related to an error while simplifying, predicting or parsing.
                                if hidden_cell == -1:
                                    raise ValueError(hidden_row_index, hidden_column_index, "Error while solving!")

                                # Computes the surrounding range of the chosen cell.
                                top_left_x = hidden_column_index
                                top_left_y = hidden_row_index
                                bottom_right_x = hidden_column_index
                                bottom_right_y = hidden_row_index

                                if hidden_column_index >= 1:
                                    top_left_x -= 1

                                if hidden_row_index >= 1:
                                    top_left_y -= 1

                                if hidden_column_index <= width -2:
                                    bottom_right_x += 1

                                if hidden_row_index <= height -2:
                                    bottom_right_y += 1

                                # Counting variables.
                                important = False
                                cell_coordinates = list()
                                b_cell_coordinates = list()
                                # pylint: disable=invalid-name
                                for y in range(top_left_y, bottom_right_y +1):
                                    for x in range(top_left_x, bottom_right_x +1):
                                        # If the coordinates x & y are the chosen cell itself...
                                        if x == hidden_column_index and y == hidden_row_index:
                                            continue

                                        # Value of the cell.
                                        hidden_value = co_hidden_matrix[y][x]

                                        # If cell still hidden...
                                        if hidden_value is None:
                                            # The main cell is important/relevant because is surrounded by
                                            # at least one hidden cell.
                                            important = True

                                            # Append the coordinates of the hidden cell as a tuple.
                                            cell_coordinates.append((x, y))

                                        # If cell is a mine...
                                        if hidden_value == "b":
                                            # Append the coordinates to a separate list.
                                            b_cell_coordinates.append((x, y))
                                            # Add it self to the equations as direct solution equation.
                                            # This is to make sure that this mine is know as a mine in the
                                            # final equation matrix.
                                            equations.add((1, tuple([(x, y)])))

                                # if the main cell is important/relevant...
                                if important:
                                    # Add the already known mines coordinates.
                                    cell_coordinates += b_cell_coordinates

                                # If there was found any surrounding hidden cells...
                                if cell_coordinates:
                                    equations.add((hidden_cell, tuple(cell_coordinates)))

                            # If the cell still hidden...
                            elif hidden_cell is None:
                                all_nones += 1

                            # If the cell is a mine...
                            elif hidden_cell == "b":
                                all_found_mines += 1

                    # Converts the type from set() to list().
                    # This is done to allow indexation.
                    equations = list(equations)

                    # Its possible that there are some duplicated equations.
                    # A set() of all equations are done, so only unique
                    # equations remaining.
                    total_objects = set()
                    for equation in equations:
                        for cell in equation[1]:
                            total_objects.add(cell)

                    # Converts the type from set() to list().
                    # This is done to allow indexation.
                    total_objects = list(total_objects)

                    # This is an positional variable.
                    extra_equation = 0
                    # If the total unique equations are equal to the total hidden cells remaining...
                    if len(total_objects) == all_nones:
                        extra_equation = 1

                    # Generates the matrices.
                    # Together, this matrices form an augmented matrix.
                    matrix_equation_variables = numpy.empty((len(equations) + extra_equation, len(total_objects)), dtype= int)
                    matrix_equation_equals = numpy.empty((len(equations) + extra_equation, 1), dtype= int)

                    # If extra equation was set as True/1...
                    if extra_equation:
                        # This add one more equation to the matrices.
                        # This equation match all mines remaining with all unique equations.
                        # This allows to known how many mines are hidden and discard imposible situations.
                        # Obviously, this is only possible in the final stages of the game.
                        equations.append((mines - all_found_mines, tuple(total_objects)))
                    if debug_level > 1:
                        pprint(equations)
                        print(total_objects)

                    # If whether or not the hidden matrix could possibly be simplified again.
                    simplificable = False

                    # This relates every equation with their unique cell.
                    for equation_index, equation in enumerate(equations):
                        for unique_cell_index, unique_cell in enumerate(total_objects):
                            # If the unique cell is one of the unique cells of the equation...
                            if unique_cell in equation[1]:
                                matrix_equation_variables[equation_index][unique_cell_index] = 1
                            else:
                                matrix_equation_variables[equation_index][unique_cell_index] = 0

                            # Adds the value of the equation to the matrix of values.
                            matrix_equation_equals[equation_index][0] = equation[0]

                        # If the current equation have an immediate solution...
                        if sum(matrix_equation_variables[equation_index]) == matrix_equation_equals[equation_index][0]:
                            simplificable = True
                    if debug_level > 1:
                        pprint(matrix_equation_variables)
                        pprint(matrix_equation_equals)

                    # Counting variables.
                    known_values = dict()
                    done_rows = list()
                    done_equations = list()
                    # This loop iterates over the equations and tries to solve them logically.
                    # This is done for these equations that are immediate, and those that
                    # would be solved thanks to the immediate.
                    while simplificable:
                        simplificable = False
                        for equation_index, equation in enumerate(equations):
                            # If the current equation have an immediate solution and was not done before...
                            if (sum(matrix_equation_variables[equation_index]) == matrix_equation_equals[equation_index][0] and
                                equation_index not in done_rows):
                                if debug_level > 1:
                                    print(equation)

                                # Mark as done equation.
                                done_rows.append(equation_index)

                                for unique_cell_index, unique_cell in enumerate(total_objects):
                                    # The state of this unique cell in the current equation.
                                    value = matrix_equation_variables[equation_index][unique_cell_index]

                                    # If the unique cell is one of the unique cells of the equation...
                                    if value:
                                        # If the current cell is not already a mine.
                                        if co_hidden_matrix[unique_cell[1]][unique_cell[0]] != "b":
                                            simplificable = True
                                        # Set this cell as known value.
                                        known_values[total_objects[unique_cell_index]] = True
                        if debug_level > 1:
                            if simplificable:
                                print(f"pre {SGR.format(known_values, SGR.Foreground.rgb(100, 100, 100))} "+
                                      f"simplificable: {SGR.format(simplificable, SGR.Foreground.green)}")
                            else:
                                print(f"pre {SGR.format(known_values, SGR.Foreground.rgb(100, 100, 100))} "+
                                      f"simplificable: {SGR.format(simplificable, SGR.Foreground.red)}")

                        for equation_index, equation in enumerate(equations):
                            # If was not done before...
                            if equation_index not in done_equations:

                                # Counting variables.
                                matches = dict()
                                not_matches = list()
                                for unique_cell_index, unique_cell in enumerate(total_objects):

                                    # The state of this unique cell in the current equation.
                                    value = matrix_equation_variables[equation_index][unique_cell_index]

                                    # If the unique cell is one of the unique cells of the equation and
                                    # was set as known value.
                                    if value and total_objects[unique_cell_index] in known_values:
                                        matches[total_objects[unique_cell_index]] = known_values[total_objects[unique_cell_index]]

                                    # If the unique cell is one of the unique cells of the equation, but
                                    # its value is unknown.
                                    elif value:
                                        not_matches.append(total_objects[unique_cell_index])

                                # The number of known mines found in this equation.
                                indices = [index for index, value in enumerate(matches.values()) if value]

                                if debug_level > 1:
                                    print(f"\nequation --> value: {SGR.format(equation[0], SGR.Foreground.rgb(100, 100, 100))} "+
                                                       f"cells: {SGR.format(equation[1], SGR.Foreground.rgb(100, 100, 100))}\n"+ 
                                          f"    matches: {SGR.format(matches, SGR.Foreground.rgb(100, 100, 100))} "+
                                              f"indices: {SGR.format(indices, SGR.Foreground.rgb(100, 100, 100))}\n"+
                                          f"    not_matches: {SGR.format(not_matches, SGR.Foreground.rgb(100, 100, 100))}")

                                # If the number of unique cells with unknown values are as much 1, or
                                # the number of known mines found in this equation is equals to the value
                                # of the equation itself...
                                if len(not_matches) <= 1 or len(indices) == equation[0]:
                                    # Mark as done equation.
                                    done_equations.append(equation_index)

                                    # If at least one unique cell with unknown value was found...
                                    if not_matches:
                                        simplificable = True

                                        if debug_level > 1:
                                            print(SGR.format(">> Simplificable!", SGR.Foreground.green))

                                        # If the number of known mines found in this equation is equals
                                        # to the value of the equation itself...
                                        if equation[0] == len(indices):
                                            known_values[not_matches[0]] = False

                                        # If not, then this is a known mine.
                                        else:
                                            known_values[not_matches[0]] = True

                        if debug_level > 1:
                            print(matches)
                            if simplificable:
                                print(f"post {SGR.format(known_values, SGR.Foreground.rgb(100, 100, 100))} "+
                                      f"simplificable: {SGR.format(simplificable, SGR.Foreground.green)}")
                            else:
                                print(f"post {SGR.format(known_values, SGR.Foreground.rgb(100, 100, 100))} "+
                                      f"simplificable: {SGR.format(simplificable, SGR.Foreground.red)}")


                    if debug_level > 1:
                        print("checking...")

                    # If there are at least one unique cell with known value...
                    if known_values:
                        # Counting variables.
                        simplified = True
                        known_mines = 0
                        for cell, value in known_values.items():

                            # If the current unique cell is a known mine...
                            if value:
                                known_mines += 1

                                # If this unique cell has not been revealed yet...
                                if co_hidden_matrix[cell[1]][cell[0]] != "b":
                                    co_hidden_matrix[cell[1]][cell[0]] = "b"

                                    # This means that the matrix could possibly be simplified further.
                                    simplified = False

                            # If the current unique cell is known as safe cell...
                            else:
                                # Reveals the real value of the cell.
                                co_hidden_matrix[cell[1]][cell[0]] = matrix[cell[1]][cell[0]]

                        # If the number of known mines are equals to the total mines, then the
                        # generated map was solved.
                        if known_mines == mines:
                            return True, co_hidden_matrix, total_objects, matrix_equation_variables, matrix_equation_equals

                    # If there are not unique cells with known values...
                    else:
                        # This cannot be simplified any further.
                        simplified = True

                    # If cannot be simplified any further.
                    if simplified:
                        # The generated map still unsolved.
                        # Let matrix operations method try for complex combinations/cases.
                        return False, co_hidden_matrix, total_objects, matrix_equation_variables, matrix_equation_equals

            # Counter variables.
            solved = False
            solving_attempts = 0
            # Start the main loop.
            while not solved and solving_attempts < 100:
                solving_attempts += 1
                if debug_level > 1:
                    print("Trying, simplifier..")
                # Call the logical simplifier. The logical simplifier has its own loop.
                solved, hidden_matrix, total_objects, matrix_equation_variables, matrix_equation_equals = simplifier(matrix, hidden_matrix)
                if debug_level > 1:
                    print_hidden(matrix)
                    print_hidden(hidden_matrix)
                # If the generated map was not solved by the logical simplifier... It could happen.
                if not solved:
                    try:
                        # Try simple matrix solving. This only works within limited range of matrices.
                        # This also does not use prediction. Only return exact results.
                        matrix_solve = numpy.linalg.solve(matrix_equation_variables, matrix_equation_equals)
                        matrix_solve = matrix_solve[0]
                    except Exception: # pylint: disable=broad-exception-caught
                        # If the given matrix is singular or not square.
                        # This solution implements prediction and approximations.
                        # This should be useful for cases with complex arrangements. Where the solution could
                        # be found thanks to knowing the remaining mines or taking into account multiple positions
                        # and discarding the impossible cases.
                        # !!! Anyway, this could use prediction and go wrong. If so, then discarded as no possible
                        # solution was found.
                        matrix_solve = numpy.linalg.lstsq(matrix_equation_variables, matrix_equation_equals, rcond=0)
                        matrix_solve = [float(i[0]) for i in list(matrix_solve[0])]

                    # Counting variables.
                    full_precision = False

                    # Iterates the solutions for every equation in the matrix.
                    for equation_resolution_index, equation_resolution in enumerate(matrix_solve):
                        # If the solution is True or very close to True...
                        if round(equation_resolution, 5) == 1.0:
                            # Checks some conditions and then set the new value to the hidden matrix.

                            # Gets the real value and hidden value.
                            hidden_cell = total_objects[equation_resolution_index]
                            real_value = matrix[hidden_cell[1]][hidden_cell[0]]
                            if debug_level > 1:
                                print(f"Computed {SGR.format('True', SGR.Foreground.green)}! -> "+
                                      f"{hidden_cell} {SGR.format(equation_resolution, SGR.Foreground.green)}")

                            # If the real value is a mine...
                            if real_value == -1:
                                # If the hidden value was already set as mine, then does not count this attempt.
                                if hidden_matrix[hidden_cell[1]][hidden_cell[0]] != "b":
                                    hidden_matrix[hidden_cell[1]][hidden_cell[0]] = "b"
                                    # Full precision prediction or exact solve was found.
                                    full_precision = True
                            # If the real value is something different from the prediction...
                            else:
                                if debug_level > 1:
                                    print("Bad prediction!")
                                # The solver predicted wrong and lost the game. No solve was found for this generated map.
                                return False, hidden_matrix

                        # If the solution is False or very close to False...
                        elif round(equation_resolution, 5) == 0.0:
                            # Full precision prediction or exact solve was found.
                            full_precision = True

                            # Gets the real value and hidden value.
                            hidden_cell = total_objects[equation_resolution_index]
                            real_value = matrix[hidden_cell[1]][hidden_cell[0]]
                            if debug_level > 1:
                                print(f"Computed {SGR.format('False', SGR.Foreground.red)}! -> "+
                                      f"{hidden_cell} {SGR.format(equation_resolution, SGR.Foreground.red)}")

                            # If the real value is not a mine...
                            if real_value != -1:
                                # Reveals the real value of the cell.
                                hidden_matrix[hidden_cell[1]][hidden_cell[0]] = real_value

                            # If the real value is a mine, opposite to the prediction...
                            else:
                                if debug_level > 1:
                                    print("Bad prediction!")
                                # The solver predicted wrong and lost the game. No solve was found for this generated map.
                                return False, hidden_matrix

                    # If no full precision prediction or exact solve was found...
                    if not full_precision:
                        if debug_level > 0:
                            print("Unable to solve!")
                        # The solver cannot continue, so it is taken for granted that no possible solution can be found.
                        return False, hidden_matrix

                    # Counts how many mines were found at the moment.
                    mine_found = 0
                    stop = False
                    for hidden_row in hidden_matrix:
                        for hidden_cell in hidden_row:
                            # If the cell still hidden/unknown.
                            if hidden_cell is None:
                                solved = False
                                stop = True
                                # There are still cells to be revealed.
                                break

                            # If the cell is a mine.
                            elif hidden_cell == "b":
                                mine_found += 1

                        # A way to spread the break statement.
                        if stop:
                            break

                    # If the mines already found are equal to the total mines. Then the map was already solved.
                    if mine_found == mines:
                        if debug_level > 1:
                            print("Was solved!")
                        return True, hidden_matrix

                    # If the map is not solved yet, then continue with the loop and try again...

                # If the map was marked as solved...
                else:
                    # Counts how many mines were found at the moment.
                    mine_found = 0
                    solved = True
                    stop = False
                    for hidden_row in hidden_matrix:
                        for hidden_cell in hidden_row:
                            # If the cell still hidden/unknown.
                            if hidden_cell is None:
                                solved = False
                                stop = True
                                # There are still cells to be revealed.
                                break

                            # If the cell is a mine.
                            elif hidden_cell == "b":
                                mine_found += 1

                        # A way to spread the break statement.
                        if stop:
                            break

                    # If the mines already found are equal to the total mines. Then the map was already solved.
                    if mine_found == mines:
                        if debug_level > 1:
                            print("Was solved!")
                        return True, hidden_matrix

                    # If the map is not solved yet.
                    # This normally shouldn't happen,
                    # but in case there was an error clearing all the remaining hidden cells,
                    # let continue with the loop and try again...
            if solved:
                return True, hidden_matrix
            else:
                return False, hidden_matrix

        def check(matrix: list, hidden_matrix: list):
            """
            check internal function

            Checks if the original matrix and the hidden_matrix (the solve) are
            equals. This prevents any uncaught and unexpected errors.

            Parameters
            ----------
            matrix : `list`
                The generated minesweeper map represented as a matrix, which in turn, is a representation of a list of lists.
            hidden_matrix : `list`
                A copy of `matrix` but with hidden values. This represents the state of the game. Works as normal game.
                This have to be in its last state, i.e. completely solved and without any hidden values.

            Returns
            -------
            `bool`
                If the given matrices are equals or not.
            """
            for hidden_row_index, hidden_row in enumerate(hidden_matrix):
                for hidden_column_index, hidden_cell in enumerate(hidden_row):
                    # If the current cell is a mine...
                    if hidden_cell == "b":
                        hidden_cell = -1

                    # If the current cell is not equals to the same cell but in the original matrix...
                    if hidden_cell != matrix[hidden_row_index][hidden_column_index]:
                        return False
            return True

        # Generates a copy of the given matrix, but with hidden values except 0/empty cells.
        has_zero = False
        hidden_matrix = list()
        for row in matrix:
            hidden_row = list()
            for cell in row:
                # If the current cell is not 0/empty...
                if cell != 0:
                    # Set None for any value, as they are hidden.
                    hidden_row.append(None)

                # If the current cell is 0/empty...
                else:
                    has_zero = True
                    # Leaves 0, emulating as if the player had clicked there.
                    hidden_row.append(0)
            hidden_matrix.append(hidden_row)
        if debug_level > 1:
            print_hidden(matrix)
            print_hidden(hidden_matrix)

        # If the matrix had at least one 0/empty cell...
        if has_zero:
            # Reveals all cells that surround 0/empty cells.
            for hidden_row_index, hidden_row in enumerate(hidden_matrix):
                for hidden_column_index, hidden_cell in enumerate(hidden_row):
                    if hidden_cell == 0:
                        top_left_x = hidden_column_index
                        top_left_y = hidden_row_index
                        bottom_right_x = hidden_column_index
                        bottom_right_y = hidden_row_index

                        if hidden_column_index >= 1:
                            top_left_x -= 1

                        if hidden_row_index >= 1:
                            top_left_y -= 1

                        if hidden_column_index <= width -2:
                            bottom_right_x += 1

                        if hidden_row_index <= height -2:
                            bottom_right_y += 1

                        # pylint: disable=invalid-name
                        for y in range(top_left_y, bottom_right_y +1):
                            for x in range(top_left_x, bottom_right_x +1):
                                if x == column_index and y == row_index:
                                    continue

                                hidden_value = hidden_matrix[y][x]

                                if hidden_value is None:
                                    hidden_matrix[y][x] = matrix[y][x]
        # If no 0/empty cells where found...
        else:
            if debug_level > 0:
                print("Too complex map!")
            return False

        if debug_level > 0:
            print("Trying solver...")
        # Executes the solver loop.
        solved, hidden_matrix = solve_simple(matrix, hidden_matrix)
        if solved:
            checked = check(matrix, hidden_matrix)
            if debug_level > 0:
                print(f"Can be solved --> {checked}")
            return checked
        else:
            if debug_level > 0:
                print("No posible solution was found...")
            return False

    # Counter variables.
    # total_mines = mines
    fails = 0
    # matrix, matrix_register = grid_generator(height, width)
    possible_solution_found = False

    if max_fails is None:
        max_fails = (height * width) ** 2

    # Main loop used to attempt every single mine placement.
    start_time = datetime.datetime.now()
    while not possible_solution_found and fails < max_fails:
        matrix, matrix_register = grid_generator(height, width)
        total_mines = mines
        while total_mines > 0 and fails < max_fails:

            # Sub_total_mines useful to acknowledge if mine were placed at any time.
            sub_total_mines = total_mines

            # Randomly choice a cell to be set as a mine.
            try:
                row_choice: list = random.choice(matrix_register)
            except IndexError:
                if debug_level > 1:
                    print("No more mines can be placed!")
                matrix, matrix_register = grid_generator(height, width)
                total_mines = mines
                row_choice: list = random.choice(matrix_register)

            cell_index: dict = random.choice(row_choice)
            row_index = cell_index["y"]
            column_index = cell_index["x"]
            value = matrix[row_index][column_index]

            # If the cell is already a mine...
            if value == -1:
                continue

            # Computes the surrounding range of the chosen cell.
            top_left_x = column_index
            top_left_y = row_index
            bottom_right_x = column_index
            bottom_right_y = row_index

            if column_index >= 1:
                top_left_x -= 1

            if row_index >= 1:
                top_left_y -= 1

            if column_index <= width-2:
                bottom_right_x += 1

            if row_index <= height -2:
                bottom_right_y += 1

            if debug_level > 0:
                # Debugging purposes.
                print(f"Trying mine on x{column_index} y{row_index}")

                if debug_level > 1:
                    placement_matrix = copy.deepcopy(matrix)
                    placement_matrix[row_index][column_index] = str(placement_matrix[row_index][column_index]) + SGR.format("?", SGR.Foreground.green)
                    discord_paste_string = str()
                    # pylint: disable=consider-using-enumerate
                    for _row_index in range(len(placement_matrix)):
                        discord_paste_string += "["
                        for _column_index in range(len(placement_matrix[_row_index])):
                            value = str(placement_matrix[_row_index][_column_index])
                            if len(value) == 1:
                                value = f" {SGR.format(value, SGR.Foreground.rgb(100, 100, 100))} "
                            else:
                                if "?" in value or "!" in value:
                                    if "-1" not in value:
                                        value = f" {value}"
                                else:
                                    value = f"{SGR.format(value, SGR.Foreground.red)} "
                            discord_paste_string += f"{value}"
                        discord_paste_string += "]\n"
                    print(discord_paste_string)

            # Conditions counter that must be met.
            conditions = {"empty": 0, "mines": 0}
            # pylint: disable=invalid-name
            for y in range(top_left_y, bottom_right_y +1):
                for x in range(top_left_x, bottom_right_x +1):

                    # If the coordinates x & y are the chosen cell itself...
                    if x == column_index and y == row_index:
                        continue

                    # First level of recursion.
                    level = 1

                    # Value of the cell.
                    value = matrix[y][x]

                    # Set chosen cell as parten of the possible surrounding mines.
                    parents = [{"x": column_index, "y": row_index}]

                    # If cell contains a mine...
                    if value == -1:
                        # Check recursively if the mine still valid.
                        if check_mine(matrix, x, y, level, parents):
                            conditions["mines"] += 1
                        else:
                            # Bad condition.
                            conditions["mines"] = 100
                            break

                    # If the cell is empty and the condition for empty cells has not yet been met...
                    if value == 0 and conditions["empty"] < 3:
                        if check_empty(matrix, x, y, level):
                            conditions["empty"] += 1
                        else:
                            continue

                # Useful statement that breaks recursion if some bad conditions are met
                # and therefore no longer matters what happens later.
                if conditions["empty"] < 0 or conditions["mines"] > 2 or conditions["mines"] < 0:
                    break

            # If conditions are met...
            if conditions["empty"] >= 3 and conditions["mines"] <= 2:
                # Set chosen cell as a mine.
                matrix[row_index][column_index] = -1
                # One mine less to place.
                total_mines -= 1

                row_choice.remove(cell_index)

                if not row_choice:
                    matrix_register.remove(row_choice)

                if debug_level > 0:
                    # Debugging purposes.
                    print(SGR.format("mine added!!", SGR.Foreground.green))
                    if debug_level > 1:
                        discord_paste_string = str()
                        # pylint: disable=consider-using-enumerate
                        for _row_index in range(len(matrix)):
                            discord_paste_string += "["
                            for _column_index in range(len(matrix[_row_index])):
                                value = str(matrix[_row_index][_column_index])
                                if len(value) == 1:
                                    value = f" {value} "
                                else:
                                    if "?" in value or "!" in value:
                                        if "-1" not in value:
                                            value = f" {value}"
                                    else:
                                        value = f"{value} "
                                discord_paste_string += f"{value}"
                            discord_paste_string += "]\n"
                        print(discord_paste_string)
                    print("\n")

            # If no mine was placed.
            if sub_total_mines == total_mines:
                # Failed attempt.
                fails += 1
                row_choice.remove(cell_index)

                if not row_choice:
                    matrix_register.remove(row_choice)
                if debug_level > 0:
                    # Debugging purposes.
                    print(SGR.format(f"Not valid mine position!! ({conditions})", SGR.Foreground.red))

        # If while loop exit without placing all mines...
        if total_mines > 0:
            if debug_level > 0:
                # Debugging purposes.
                print(f"Time execution: {(datetime.datetime.now() - start_time).total_seconds()}")
            raise RecursionError(fails, f"Too many mines! Total: {mines} Remaining: {total_mines} Fails: {fails}")

        # If all mines were placed...
        # pylint: disable=consider-using-enumerate
        # Iterates the matrix to set the correct values for mines surroundings.
        for row_index in range(len(matrix)):
            for column_index in range(len(matrix[row_index])):

                # The value of the cell.
                value = matrix[row_index][column_index]

                # If cell contains a mine...
                if value == -1:
                    # Computes the surrounding range of the cell.
                    top_left_x = column_index
                    top_left_y = row_index
                    bottom_right_x = column_index
                    bottom_right_y = row_index

                    if column_index >= 1:
                        top_left_x -= 1

                    if row_index >= 1:
                        top_left_y -= 1

                    if column_index <= width-2:
                        bottom_right_x += 1

                    if row_index <= height -2:
                        bottom_right_y += 1

                    # pylint: disable=invalid-name
                    for y in range(top_left_y, bottom_right_y +1):
                        for x in range(top_left_x, bottom_right_x +1):

                            # If the coordinates x & y are the mine cell itself...
                            if x == column_index and y == row_index:
                                continue

                            # Value of the surrounding cell.
                            value = matrix[y][x]

                            # If surrounding cell does not contain a mine...
                            if value != -1:
                                matrix[y][x] += 1
        if height * width <= 10000:
            try:
                if solver(matrix, debug_level):
                    possible_solution_found = True
                    checked_solution = True
            except ValueError:
                pass
        else:
            possible_solution_found = True
            checked_solution = False


    # Preparation to payload the result.
    payload = {}

    if debug_level > 1:
        # Debugging purposes.
        pprint(matrix)
        print("")
        pprint(matrix_register, compact= True)
        print("\n")
    # If matrix is required...
    if "matrix" in parts_list:
        payload["matrix"] = matrix

    # if mines count is required...
    if "mines" in parts_list:
        payload["mines"] = mines

    # if discord paste format or decorated matrix is required...
    if "discord_paste" in parts_list or "decorated_matrix" in parts_list or final_report:
        discord_paste_string = str()
        decorated_matrix_string = str()

        # Iterates the matrix to perform formatting operations.
        # pylint: disable=consider-using-enumerate
        for row_index in range(len(matrix)):
            # If decorated matrix is required...
            if "decorated_matrix" in parts_list or final_report:
                # Prepares the decorated matrix string to be formatted.
                decorated_matrix_string += f"{SGR.format('[', SGR.Foreground.rgb(100, 100, 100))} "

            for column_index in range(len(matrix[row_index])):
                # Value of the cell.
                value = matrix[row_index][column_index]

                # If discord paste format is required...
                if "discord_paste" in parts_list:
                    discord_paste_string += f"||{discord_emoji_table[value]}||"

                # If cell contains a mine...
                if value == -1:
                    value = SGR.format("@", SGR.Foreground.green)

                # If cell does not surround any mine...
                elif value == 0:
                    value = " "

                # If cell surround one or more mines...
                else:
                    # Adds the value with SGR color, red-orange gradient based on value.
                    value = SGR.format(value, SGR.Foreground.rgb(255, 200 - (25 * value), 0))

                # If decorated matrix is required...
                if "decorated_matrix" in parts_list or final_report:
                    decorated_matrix_string += f"{value} "

            # If discord paste format is required...
            if "discord_paste" in parts_list:
                discord_paste_string += "\n"

            # If decorated matrix is required...
            if "decorated_matrix" in parts_list or final_report:
                # Closes the decorated matrix string formatting.
                decorated_matrix_string += SGR.format("]\n", SGR.Foreground.rgb(100, 100, 100))

        if "discord_paste" in parts_list:
            payload["discord_paste"] = discord_paste_string
        if "decorated_matrix" in parts_list or final_report:
            payload["decorated_matrix"] = decorated_matrix_string
            if debug_level > 1 or final_report:
                print(decorated_matrix_string)

    if debug_level > 1 or final_report or "metadata" in parts_list:
        # Debugging purposes.
        matrix_size = sys.getsizeof(matrix)
        matrix_register_size = sys.getsizeof(matrix_register)
        string_size = sys.getsizeof(discord_paste_string)
        string2_size = sys.getsizeof(decorated_matrix_string)
        total_size = (matrix_size + string_size + string_size + matrix_register_size) / (1024*1024)
        if total_size >= 1:
            total_size = round(total_size, 2)
        else:
            final_number = "0."
            decimal = str(total_size).split(".")

        total_decimals = 0
        for i in decimal[1]:
            if i == "0":
                final_number += "0"
            else:
                total_decimals += 1
                final_number += i
            if total_decimals >= 2:
                break
        total_size = float(final_number)
        if "metadata" in parts_list:
            payload["metadata"] = {
                "fails": fails,
                "verified": checked_solution,
            }

        if debug_level > 1 or final_report:
            print(f"Time execution: {(datetime.datetime.now() - start_time).total_seconds()}\n"+
                f"Verified possible solution?: {checked_solution}\n"+
                f"Fails: {fails}\n"+
                f"mines: {mines}\n"+
                f"Matrix Size: {matrix_size}\n"+
                f"Matrix Register Size: {matrix_register_size}\n"+
                f"Discord Paste Size: {string_size}\n"+
                f"Decorator Size: {string2_size}\n"+
                f"Total Size: {total_size} MB")

    # Returns the payload.
    return payload
