import discord
from discord.commands import slash_command
from discord.ext import commands

from p_modules import get
from p_modules.graphical.embeds import Embed
import cogs.events.modules.verification as verification_module
from p_modules.database.main import Database
import asyncio


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        THIS REQUIRES AN BACKEND WHICH ALLOWS AUTHORISATION
        YOU NEED TO FIND AN WAY YOURSELF TO IMPLEMENT AN BACKEND WITH THIS PART
        if needed, contact Mathcel [Bot Dev] or => X3CF / Herrtt [Front & Backend Devs]
        """
        time = get.config('time')
        guild = self.bot.get_guild(get.config('gid')[0])
        role = guild.get_role(1015311224684171325)   # 1002691224538447959
        info = guild.get_channel(1015301454334009434)   # 883093944743886939
        notification = guild.get_channel(1015301454334009434)   # 996761316041703556
        media = guild.get_channel(1015301454334009434)   # 927713912865046548

        ping_message = await info.send('<@{}>'.format(member.id))
        await ping_message.delete()

        fetch_user = await verification_module.fetch_user_entry(member)
        if fetch_user['status'] == 200:
            if fetch_user['returnValue']['s_flag'] == 1:
                # await member.add_roles(role)
                description = '**You are verified\nYou received `Member` role\nWelcome to Boronide.**'
                send_dm = await verification_module.send_dm(member, description=description, title='Verification System')
                if send_dm['status'] == 100:
                    description = 'Please turn your dm\'s on for Boronide'
                    embed = Embed.info(description=description, title='Verification System')
                    await media.send('<@{}>'.format(member.id))
                    await media.send(embed=embed)
                return await member.add_roles(role)
        elif fetch_user['status'] == 100:
            await verification_module.create_entry(member)

        url = 'https://boronide.de/api/discord/connect'
        description = '**Please authorize and verify via**\n||**{}**||\nYou have {} seconds'.format(url, time)
        send_dm = await verification_module.send_dm(member, description=description, title='Verification System')
        if send_dm['status'] == 100:
            description = '''
            <@{}> Your DMs are closed, please turn on your DMS for this Server (required for many instances)
            After you've done that, you can rejoin to restart the process. To fasten it up:
            Authorize your Discord with the link:
            https://boronide.de/api/discord/connect/
            Doing that will immediately grant you access to the Server after rejoining.
            DMS are required for: Purchases, Punishment System, Verification System
            '''.format(member.id)
            embed = Embed.info(description=description, title='Verification System')
            await notification.send(embed=embed)
        verification_results = await verification_module.start_verification_process(member)
        if verification_results['status'] == 100:
            description = 'The timer run out and you still haven\'t verified\nRejoin via ||**discord.gg/boronide**||'
            await verification_module.send_dm(member, description=description, title='Verification System')
            return await member.kick(reason=verification_results['returnValue'])
        return await member.add_roles(role)


def setup(bot):
    bot.add_cog(Verification(bot))
