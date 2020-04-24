import discord
import os
import json
import datetime
from discord.ext import commands


cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config2.json")
config = json.loads(open(jsonPath, "r").read())


class Info_commands(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Info_commands(client))
    