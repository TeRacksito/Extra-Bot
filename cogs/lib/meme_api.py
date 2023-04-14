"""
A basic implementation of the Meme API from D3vd.
"""
import json
import time

import requests


def gen_meme() -> str:
    """
    gen_meme function

    Uses the Meme API from D3vd to generate a SFW meme.

    Returns
    -------
    `str`
        A string representation of link.
    """
    url = "https://meme-api.com/gimme"

    # Attempt the meme generation up to 5 times.
    attempts = 0
    while attempts < 5:
        response = requests.get(url, timeout= (5, 10))
        content = json.loads(response.text)

        # If the meme is NSFW, then try again.
        if content["nsfw"]:
            attempts += 1
            time.sleep(0.5) # Rate Limiting Time
            continue
        return content["url"]

    # If all meme generation attempts were NSFW, then meme_blocked image is send.
    return "https://cdn.discordapp.com/attachments/1027493896055439360/1068566682571919421/meme_blocked.png"
