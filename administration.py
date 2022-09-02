import discord
from discord.commands import slash_command
from discord.ext import commands

from p_modules import get
from p_modules.graphical.embeds import Embed
import cogs.commands.modules.administration as administration_module
from p_modules.database.main import Database


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=get.config('gid'), description='Ban a user from Boronide')
    async def ban(self, ctx, user: discord.Member, reason):
        if await administration_module.check_permissions(ctx) is None:
            embed = Embed.info(description='**M_FLAG: `0x2` | [Moderator] Required!**', title='Permissions Level too low')
            return await ctx.respond(embed=embed)

        if ctx.author.id == user.id:
            embed = Embed.error(description='||**`Can\'t ban yourself`**||', title='Invalid Ban Action')
            return await ctx.respond(embed=embed)

        if await administration_module.check_ban(user) is None:
            embed = Embed.error(description='||User <@{}>is already banned||'.format(user.id), title='Invalid Ban Target')
            return await ctx.respond(embed=embed)

        author_permissions = await administration_module.fetch_user_entry(ctx.author)
        target_permissions = await administration_module.fetch_user_entry(user)
        if target_permissions['status'] == 200:
            target_m_flag = target_permissions['returnValue']['m_flag']
            if author_permissions['returnValue']['m_flag'] <= target_m_flag:
                description = 'Permissions level is too low\nCan not ban User [<@{}>]'.format(user.id)
                embed = Embed.error(description=description, title='Permission level too low')
                return await ctx.respond(embed=embed)

        try:
            description = '''
            **<@{}> — [{}] Permanently banned you from Boronide
            Reason:\n```\n{}\n```\nAppeal Server: https://discord.gg/boronide
            '''.format(ctx.author.id, ctx.author.id, reason)
            embed = Embed.plain(description=description, title='Banned from Boronide')
            await ctx.send(embed=embed)
        except Exception as e:
            return await ctx.respond(embed=Embed.error(description='||**`{}`**||'.format(e)))

        try:
            fetched_guild = await self.bot.fetch_guild(get.config('gid')[0])
            await fetched_guild.ban(user, reason=reason, delete_message_days=1)
        except Exception as e:
            return await ctx.respond(embed=Embed.error(description='||**`{}`**||'.format(e)))

        client = Database.connect_to_database(get.config('mongodb'))
        collection = Database.get_collection(client, 'BoronideUserDB', 'Bans')
        Database.create_entry(collection, {'_id': user.id, 'reason': reason})

        description = '**Successfully banned User:\n<@{}>**'.format(user.id)
        embed = Embed.plain(description=description, title='Ban Command')
        await ctx.respond(embed=embed)

    @slash_command(guild_ids=get.config('gid'), description='Unban a user from Boronide')
    async def unban(self, ctx, user: discord.Member):
        if await administration_module.check_permissions(ctx) is None:
            embed = Embed.info(description='**M_FLAG: `0x2` | [Moderator] Required!**', title='Permissions Level too low')
            return await ctx.respond(embed=embed)

        if ctx.author.id == user.id:
            embed = Embed.error(description='||**`How do you want to unban yourself? Lol`**||')
            return await ctx.respond(embed=embed)

        try:
            fetched_guild = await self.bot.fetch_guild(get.config('gid')[0])
            await fetched_guild.unban(user, reason='Unbanned by {}'.format(ctx.author))
        except Exception as e:
            return await ctx.respond(embed=Embed.error(description='||**`{}`**||'.format(e)))

        client = Database.connect_to_database(get.config('mongodb'))
        collection = Database.get_collection(client, 'BoronideUserDB', 'Bans')
        delete_entry = Database.delete_entry(collection, '_id', user.id)
        if delete_entry['status'] == 100:
            embed = Embed.error(description=delete_entry['returnValue'], title='Error with Unbanning')
            return await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Administration(bot))
