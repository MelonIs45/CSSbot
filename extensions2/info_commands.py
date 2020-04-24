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

    @commands.command(help = "**`$help <command>`**",
    brief = "Specify a command and it will tell you information on how to properly use it.",
    usage = "**Usage: `$help <command>`**",
    description = "Hmm are you that much of a melon to understand???\n\nExample: `$help ping`"
    )
    async def help(self, ctx, r_command = None):
        utils = self.client.get_cog("Utils")
        member = ctx.guild.get_member(ctx.author.id)
        if r_command is None:
            embed = discord.Embed()
            utils.get_member(ctx, member)
            utils.create_embed(ctx, embed, member)
            embed.title = "CSSbot Help"
            for command in self.client.commands:
                if command.help is None:
                    pass
                else:
                    embed.add_field(name = command.help, value = command.brief, inline = False)
            embed.set_author(name = "")
            await ctx.channel.send(embed = embed)
        else:
            for command in self.client.commands: 
                if command.name == r_command:
                    embed = discord.Embed()
                    utils.get_member(ctx, member)
                    utils.create_embed(ctx, embed, member)

                    embed.title = "CSSbot Help"
                    embed.add_field(name = command.usage, value = command.description, inline = False)
                    embed.set_author(name = "")

                    await ctx.channel.send(embed = embed) 
                else:
                    await ctx.send("Unable to find command!")       


    @commands.command(help = "**`$ping`**",
    brief = "Returns ping in ms.",
    usage = "**Usage: `$ping`**",
    description = "Returns the client latency in milliseconds, no arguments are to be given.\n\nExample: `$ping`"
    )
    async def ping(self, ctx):
        utils = self.client.get_cog("Utils")
        client = self.client
        member = None

        if ctx.author == client.user:
            return

        embed = discord.Embed()
        utils.get_member(ctx, member)
        utils.create_embed(ctx, embed, member)
        embed.set_author(name = "")
        embed.description = 'Pong! {0}ms'.format(round((client.latency)*1000, 1))

        await ctx.send(embed = embed)  


def setup(client):
    client.add_cog(Info_commands(client))
    