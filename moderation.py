import discord
from discord.commands import slash_command
from discord.ext import commands

from p_modules import get
from p_modules.graphical.embeds import Embed
import cogs.commands.modules.moderation as moderation_module

import re


async def check_permissions(ctx):
    read = await moderation_module.fetch_user_entry(ctx.author)
    if not await moderation_module.check_user_permissions(ctx, read):
        return None
    return 0


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=get.config('gid'), description='Call a method for the user database')
    async def entry(self, ctx, method, user: discord.Member, email):
        if await check_permissions(ctx) is None:
            embed = Embed.info(description='**M_FLAG: `0x2` | [Moderator] Required!**', title='Permissions Level too low')
            return await ctx.respond(embed=embed)

        methods = ['create', 'delete']
        if method not in methods:
            description = 'Method: {}\nIs not equal to Methods: {}'.format(method, methods)
            embed = Embed.error(description=description, title='Invalid Method')
            return await ctx.respond(embed=embed)

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            embed = Embed.error(description='||**Email:\n{}\nIs Invalid**||'.format(email), title='Invalid Email')
            return await ctx.respond(embed=embed)

        process_method = await moderation_module.process_method(ctx, method, user, email)
        if process_method['status'] == 200:
            embed = Embed.plain(description=process_method['returnMessage'], title='Successful Action')
            return await ctx.respond(embed=embed)

    @slash_command(guild_ids=get.config('gid'), description='Purge a specific amount of messages.')
    async def purge(self, ctx, amount):
        if await check_permissions(ctx) is None:
            embed = Embed.info(description='**M_FLAG: `0x2` | [Moderator] Required!**', title='Permissions Level too low')
            return await ctx.respond(embed=embed)

        if not all(digit in '0123456789' for digit in amount):
            description = '||**Input: `{}` contains illegal characters: please only use numbers**||'
            embed = Embed.error(description=description, title='Purge Command Error')
            return await ctx.respond(embed=embed)

        if int(amount) >= 100:
            description = 'Delete Amount {} is too big [{}]\nSetting amount to 100'.format(amount, int(amount)-100)
            amount = '100'
            await ctx.respond(embed=Embed.warn(description=description))

        description = '**<@{}>\nPurging `{}` Messages\n**'.format(ctx.author.id, amount)
        await ctx.respond(embed=Embed.plain(description=description, title='Successful Command'))
        await ctx.channel.purge(limit=int(amount), bulk=True)
        

def setup(bot):
    bot.add_cog(Moderation(bot))
