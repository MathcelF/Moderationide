import discord
from discord.commands import slash_command
from discord.ext import commands

from p_modules import get
from p_modules.graphical.embeds import Embed
from p_modules.database.main import Database
import asyncio


class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if any(item in message.content.split() for item in ["-obf", "-obfuscate", "```lua"]):
            return 0
        if message.author.id in [1010993858257109082, 1010993858257109082]:
            return None
        channel = self.bot.get_channel(get.config("lig"))
        if str(message.channel) == 'Direct Message with Unknown User':
            description = '**DMs: <@{}>\nContent:\n```\n{}\n```**'.format(message.author.id, message.content)
        else:
            description = '**Channel:\n{}\nContent:\n```\n{}\n```**'.format(message.channel.mention, message.content)
        embed = Embed.logging_embed(description=description, title='Message Edited', user=message.author)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.id == 932320101489836073:
            return None

        channel = self.bot.get_channel(get.config("lig"))
        print(before.channel)
        if str(before.channel) == 'Direct Message with Unknown User':
            description = '''
            **DMs: <@{}>\nOriginal:\n```\n{}\n```\nNew:\n```\n{}\n```**
            '''.format(before.author.id, before.content, after.content)
        else:
            description = '''
            **Channel:\n{}\nOriginal:\n```\n{}\n```\nEdited:\n```\n{}\n```**
            '''.format(before.channel.mention, before.content, after.content)
        embed = Embed.logging_embed(description=description, title='Message Edited', user=before.author)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Logging(bot))
