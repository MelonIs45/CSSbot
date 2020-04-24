import discord
import os
import json
import datetime
import asyncio
import time
import traceback
import sys
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


    @commands.command()
    async def request(self, ctx, name, school):
        client = self.client
        if ctx.channel.id == int(config["verify"]["requestChannel"]) and len(ctx.message.content.split(" ")) == 3:
            guild = client.get_guild(ctx.guild.id)
            verifyChannel = guild.get_channel(int(config["verify"]["verifyChannel"]))
            await verifyChannel.send(f"Name: {name}, School: {school}, User ID: {ctx.author.id}")
            await ctx.send("Request Sent!")
            await asyncio.sleep(3)
            await ctx.channel.purge(limit = 2)
        else:
            await ctx.send("Please use the format: `%request <name> <school>`")
            await asyncio.sleep(5)
            await ctx.channel.purge(limit = 2)

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def verify(self, ctx, name, school, id):
        guild = self.client.get_guild(ctx.guild.id)
        utils = self.client.get_cog("Utils")
        if ctx.channel.id == int(config["verify"]["verifyChannel"]):
            member = guild.get_member(int(id))
            role = guild.get_role(703319133973905428)
            await member.remove_roles(role)
            await ctx.send(f"Added {member} to the name list!")
            nameChannel = guild.get_channel(int(config["verify"]["nameChannel"]))
            verifyChannel = guild.get_channel(int(config["verify"]["verifyChannel"]))
            member = None
            utils.get_member(ctx, member)
            embed = discord.Embed()
            timeNow = (datetime.datetime.now()).strftime("%A %d %B %Y at %X%p")

            embed.add_field(name = "Name:", value = name, inline = True)
            embed.add_field(name = "Tag:", value = f"<@{id}>", inline = True)
            embed.add_field(name = "School:", value = school, inline = False)
            embed.set_footer(text = f"Verified at: {timeNow}")
            
            await nameChannel.send(embed = embed)



    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.UnexpectedQuoteError):
    #         await ctx.send("Please remove any quotation marks from command.")
    #         await asyncio.sleep(3)
    #         await ctx.channel.purge(limit = 2)
    #     elif isinstance(error, commands.MissingPermissions):
    #         await ctx.send("Missing permissions.")
    #     elif isinstance(error, commands.NotOwner):
    #         await ctx.send("You aren't the bot owner :D")
    #     else:
    #         exc_info = sys.exc_info()
    #         traceback.print_exception(*exc_info)
    #         del exc_info



def setup(client):
    client.add_cog(Info_commands(client))