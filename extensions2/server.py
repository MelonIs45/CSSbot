import discord
import os
import json
import datetime
from discord.ext import commands


cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config2.json")
config = json.loads(open(jsonPath, "r").read())


roleDict = {
    "🔴": "702583030031581274",
    "🟠": "702583081499885638",
    "🟡": "702583133819633715",
    "🟢": "702583173283971172",
    "🔵": "702583226249642044",
    "🟣": "702583276031705319",
    "702935881123627039": "702583638637674517"
}


class Info_commands(commands.Cog):
    def __init__(self, client):
        self.client = client


    #NOTE: Function to readd reactions to role menu incase they get removed
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     client = self.client
    #     emote = client.get_emoji(702935881123627039)
    #     for i in roleDict:
    #         try:
    #             await message.add_reaction(i)
    #         except:
    #             await message.add_reaction(emote)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        client = self.client

        messageId = payload.message_id
        channelId = payload.channel_id
        member = payload.member
        emoji = payload.emoji
        guildId = payload.guild_id
        guild = client.get_guild(guildId)

        if channelId == int(config["roleMenu"]["roleChannel"]) and messageId == int(config["roleMenu"]["roleMessage"]):
            for emote in roleDict:
                try:
                    if emoji.id == int(emote):
                        role = guild.get_role(int(roleDict[emote]))
                        await member.add_roles(role)
                except Exception:
                    if emoji.name == emote:
                        role = role = guild.get_role(int(roleDict[emote]))
                        await member.add_roles(role)
        

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        client = self.client
        
        messageId = payload.message_id
        channelId = payload.channel_id
        emoji = payload.emoji
        guild = client.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if channelId == int(config["roleMenu"]["roleChannel"]) and messageId == int(config["roleMenu"]["roleMessage"]):
            for emote in roleDict:
                try:
                    if emoji.id == int(emote):
                        role = guild.get_role(int(roleDict[emote]))
                        await member.remove_roles(role)
                except Exception:
                    if emoji.name == emote:
                        role = role = guild.get_role(int(roleDict[emote]))
                        await member.remove_roles(role)


def setup(client):
    client.add_cog(Info_commands(client))