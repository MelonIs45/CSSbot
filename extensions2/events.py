import discord
import os
import json
import datetime
import sys
from discord.ext import commands, tasks


cwd = os.path.dirname(__file__)
jsonPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config2.json')
config = json.loads(open(jsonPath, "r").read())


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        client = self.client
        print(f"-----------\nBot made by MelonIs45#8078 and Matthew -#0920\nLogged in as: {client.user.name}\nReady!")


    @commands.Cog.listener()
    async def on_message(self, message):
        global embed
        embed = discord.Embed(color = message.author.color)
        utils = self.client.get_cog("Utils")
        client = self.client
        member = message.guild.get_member(message.author.id)

        masterChannelId = client.get_channel(int(config['log']['channelId']))
        if message.guild.id == int(config['log']['logGuild']) and message.author != client.user:
            if len(message.attachments) > 0:
                attUrl = "".join(str(x) for x in message.attachments)
                attUrl = attUrl.split(" ")[3]
                attUrl = attUrl.lstrip("url='").rstrip("'>'")
                logText = "{0} {1}".format(message.content, attUrl)
            else:
                attUrl = ""
                logText = message.content

            log = open("log2.txt", "a")
            logName = message.author.display_name
            currentDT = datetime.datetime.now()
            logTime = currentDT.strftime("%Y-%m-%d %H:%M:%S")
            logFull = "{0} | {1} | {2}".format(logTime, logName, logText)
            log.write(logFull + "\n")

            utils.create_embed(message, embed, member)    
            embed.description = f"{message.content} {attUrl}"
            embed.set_footer(text = f"Sent by {member}", icon_url = member.avatar_url_as(format='png'))

            await masterChannelId.send(embed = embed)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        global embed
        embed = discord.Embed(color = message.author.color)
        utils = self.client.get_cog("Utils")
        client = self.client
        member = message.guild.get_member(message.author.id)

        masterChannelId = client.get_channel(int(config['log']['channelId']))
        if message.guild.id == int(config['log']['logGuild']):
            if len(message.attachments) > 0:
                attUrl = "".join(str(x) for x in message.attachments)
                attUrl = attUrl.split(" ")[3]
                attUrl = attUrl.lstrip("url='").rstrip("'>'")
                logText = f"Message: {message.content} {attUrl} deleted in #{message.channel.name}"
            else:
                attUrl = ""
                logText = f"Message: {message.content} deleted in #{message.channel.name}"

            utils.create_embed(message, embed, member)    
            embed.description = f"{logText}"
            embed.set_footer(text = f"Sent by {member}", icon_url = member.avatar_url_as(format='png'))

            await masterChannelId.send(embed = embed)


def setup(client):
    client.add_cog(Events(client))
