"""
Values module

A module that implements a Data Fetcher.

Raises
------
`KeyError`
    This module could raise a `KeyError` exception in some cases.
"""

import json
import os
import traceback
from types import SimpleNamespace as SN
from typing import Union

import tomli

from cogs.lib.terminal import error


class DataFetcher:
    """
    A data fetcher, can retrieve data from `.json` and `.toml` file formats.

    Use the `DataFetcher.get()` function to use the data fetcher.
    """
    def __init__(self):
        pass

    def load_json_data(self, filename: str = "data.json", encoding: str = "utf-8") -> Union[dict, any]:
        """
        load_json_data function

        Open a `.json` file and load its data.

        Parameters
        ----------
        filename : `str, optional`
            The path to the specific data file, by default `"data.json"`.
        encoding : `str, optional`
            The encoding method used to read the file, by default `"utf-8"`.

        Returns
        -------
        `dict | any`
            Returns the data saved in the file.
        """

        try:
            with open(file= filename, mode= "r", encoding= encoding, errors= "strict") as file:
                data = json.load(file)
                data = SN(**data)
            return data
        except ValueError as exception:
            error(exception, traceback.format_exc())

    def load_toml_data(self, filename: str = "config.toml") -> Union[dict, any]:
        """
        load_toml_data function

        Open a `.toml` file and load its data.

        Parameters
        ----------
        filename : `str, optional`
            The path to the specific data file, by default `"config.toml"`.

        Returns
        -------
        dict | any
            Returns the data saved in the file.
        """

        try:
            with open(file= filename, mode= "rb") as file:
                data = tomli.load(file)
                data = SN(**data)
            return data
        except ValueError as exception:
            error(exception, traceback.format_exc())

    def find_key(self, key_objective: str, dictionary: dict) -> Union[dict, None, any]:
        """
        find_key function

        Search a specific `key` on a given `dictionary`.

        If the `key` is not found in the first layer of the
        `dictionary`, then the next layer is acceded until
        the `key` is found or no more layers are available.
        If the `key` does not exist in the given `dictionary`
        then `None` is returned.

        Parameters
        ----------
        key_objective : `str`
            The `key` looked up in the `dictionary`.
        dictionary : `dict`
            The `dictionary` where the search will be performed.

        Returns
        -------
        `dict | None | any`
            Returns the data found in the `dictionary` attached to
            the specific `key`. If the `key` does not exist in the
            given `dictionary` then `None` is returned.
        """
        for key, value in dictionary.items():
            if key == key_objective:
                return value
            elif isinstance(value, dict):
                result = self.find_key(key_objective, value)
                if result is not None:
                    return result
        return None
    def generate_payload(self, key: str, data: dict) -> Union[dict, None, any]:
        """
        generate_payload function

        Handles `find_key()` function.

        `generate_payload()` function is not meant to use
        outside the `DataFetcher`.

        Parameters
        ----------
        key : `str`
            The `key` looked up in the `data`.
        data : 'dict'
            The `dictionary` where the search will be performed.

        Returns
        -------
        `dict | None | any`
            Returns the data found in the `dictionary` attached to
            the specific `key` as the final payload. If `find_key()`
            function returns `None`, then also `None` is returned and
            an exception is raised.

        Raises
        ------
        `KeyError`
            If `find_key()` function returns `None`, then a `KeyError`
            exception is raised.
        """

        payload = self.find_key(key, data)

        if payload is None:
            try:
                raise KeyError(data)
            except KeyError as exception:
                error(exception, traceback.format_exc(), )
        return payload


    @classmethod
    def get(cls, key: str, search: str | None = None) -> Union[dict, None, any]:
        """
        `@classmethod`

        get function

        Attempts to retrieve a `key` from a specific data file. If `search`
        is not specified, then a default search strategy is performed through
        the defaults data.json and config.toml files.

        Parameters
        ----------
        key : `str`
            The specific key wanted from the data. Data is treated as a normal
            dictionary.
        search : `str | None, optional`
            The path to the specific data file where the search is going to be
            performed, by default None.

            Remember that only .json and .toml file formats are supported. If
            you want to search other file formats, then you must `open()` the
            file manually.

        Returns
        -------
        `dict | None | any`
            Returns the `value` attached to the `key` on the data. If the
            `key` is not found in the data from the specific file, then
            `None` is returned and an exception is raised.
        
        Raises
        ------
        `KeyError`
            If the `key` is not found in the data from the specific
            file, then a `KeyError` exception is raised.
        """
        if search is None:
            # Default payload configuration.
            try:
                # data.json loading
                data = cls.load_json_data(self= cls)
                guilds_id = [guild["id"] for guild in data.guilds.values()]
                embeds = data.embeds
                prefix = data.metadata["prefix"]
            except TypeError:
                # No data where found...
                guilds_id = None
                embeds = None
                prefix = "-"

            try:
                # config.toml loading
                config = cls.load_toml_data(self= cls)
                token = config.options["bot_token"]
                if token == "":
                    tkn = config.options.bot_token_env
                    token = os.environ.get(tkn)
            except Exception as exception: # pylint: disable=broad-exception-caught
                # No data where found...
                error(exception, traceback.format_exc(),
                      "Impossible to define the bot's token.",
                      "Please make sure there is nothing wrong with the toml config file.",
                      level= "CRITICAL")
                token = None

            payload = {
                "guilds_id": guilds_id,
                "embeds": embeds,
                "prefix": prefix,
                "token": token
            }

            return payload.get(key.lower())

        else:
            # Custom payload configuration.

            # .json file search support.
            if search.endswith(".json"):
                data = cls.load_json_data(self= cls, filename= search)

            # .json file search support.
            elif search.endswith(".toml"):
                data = cls.load_toml_data(self= cls, filename= search)
            
            # Could be added new file format's support.

            payload = cls.generate_payload(self= cls, key= key, data= data)
            return payload
