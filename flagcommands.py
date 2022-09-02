import discord
from discord import Option
from discord.commands import slash_command
from discord.ext import commands
from p_modules import get
from p_modules.graphical.embeds import Embed
from p_modules.utilities.flag import Flag
import cogs.commands.modules.flagcommands as flag_module


class FlagAdvanced(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=get.config('gid'), description='Updates the Flags m/s of a User!')
    async def update_user_flag(self, ctx, method, user: discord.Member, flag_type, flag):
        # Fetching User Entry and checking if he has the Imperator Flag (s_flag: 0x8)
        read = await flag_module.fetch_user_entry(ctx.author)
        if not await flag_module.check_user_permissions(ctx, read):
            embed = Embed.info(description='**S_FLAG: `0x8` | [Imperator] Required!**', title='Permissions Level too low')
            return await ctx.respond(embed=embed)

        methods = ['add', 'sub']
        if method not in methods:
            description = 'Method: {}\nIs not equal to Methods: {}'.format(flag_type, methods)
            embed = Embed.error(description=description, title='Invalid Method')
            return await ctx.respond(embed=embed)

        condition = ['m_flag', 's_flag']
        if flag_type not in condition:
            description = 'Flag Option: {}\nIs not equal to Options: {}'.format(flag_type, condition)
            embed = Embed.error(description=description, title='Invalid FlagType')
            return await ctx.respond(embed=embed)
        validate_type = Flag.Get.validate_type(flag)
        if validate_type['status'] == 100:
            hexadecimal = '0123456789abcdefABCDEF'
            description = '{}\nValid Hexadecimal Characters: {}'.format(validate_type['returnValue'], hexadecimal)
            embed = Embed.error(description=description, title='Invalid Hexadecimal Character')
            return await ctx.respond(embed=embed)

        if validate_type['returnValue'] == 'hex':
            if int(flag, base=16) > int('0xF', base=16):
                description = 'Hex: {} to big by: {}'.format(flag, int(flag, base=16) - int('0xF', base=16))
                embed = Embed.error(description=description, title='Hexadecimal too big')
                return await ctx.respond(embed=embed)
            flag = int(flag, base=16)

        # Importing a function to process the type and getting the hex.
        # Importing it for OOP reasons.
        return_f = await flag_module.process_type(validate_type, flag)

        if return_f['status'] == 100:
            embed = Embed.error(description=return_f['returnValue'], title='Error with Flag')
            return await ctx.respond(embed=embed)
        if return_f['status'] == 200:
            flag = return_f['returnValue']

        # Same thing as above: Function to fetch the Database Entry from a User -> Fetching Flag.
        read = await flag_module.fetch_user_entry(user)

        user_flag = None
        if read['status'] == 200:
            user_flag = read['returnValue'][flag_type]

        if read['status'] == 100:
            embed = Embed.error(description='||{}||'.format(read['returnValue']), title='Could not read User\'s Entry')
            return await ctx.respond(embed=embed)
        if user_flag is None:
            embed = Embed.error(description='Could not fetch user\'s flag', title='Error fetching User\'s Flag')
            return await ctx.respond(embed=embed)

        flag = await flag_module.process_by_method(method, ctx, user_flag, flag, flag_type, user)
        if method == 'add':
            user_flag += flag
        await flag_module.manipulate_flags(flag_type, flag, user)

    @slash_command(guild_ids=get.config('gid'), description='Updates the Flags m/s of a User!')
    async def user_info(self, ctx, user: Option(discord.Member, 'View User\'s Information') = None):
        user = ctx.author if user is None else user
        return_entry = await flag_module.fetch_user_entry(user)
        if return_entry['status'] == 100:
            description = '<@{}> has no database entry!\nReason: ||**`User is not verified; He has to open a Ticket!`**||'.format(user.id)
            if user == ctx.author:
                description = 'You have no database entry!\nReason: ||**`You are not verified: Open a Ticket`**||\n{}'
                description.format('Exception/Error: ||**`{}`**||'.format(return_entry['returnValue']))
            embed = Embed.error(description=description, title='Error fetching User Information')
            return await ctx.respond(embed=embed)

        m_flag = return_entry['returnValue']['m_flag']
        s_flag = return_entry['returnValue']['s_flag']
        m_roles = [roles.capitalize() for roles in Flag.Get.flag_permissions(m_flag, 'm_flag')]
        s_roles = [roles.capitalize() for roles in Flag.Get.flag_permissions(s_flag, 's_flag')]

        m_string = '**`{}`**'.format(' '.join(m_roles))
        if len(m_roles) < 1:
            m_string = '**`None`**'
        s_string = '**`{}`**'.format(' '.join(s_roles))

        m_hex = hex(m_flag)[2:].upper()
        s_hex = hex(s_flag)[2:].upper()
        # Embed has a colour which should be influenced by the User's Flag:
        # E.g.  8DF8FD by s_hex = 8, m_hex = D
        colour_by_hex = '0x{}{}F{}F{}'.format(s_hex, m_hex, s_hex, m_hex)

        return_bans = await flag_module.fetch_bans(user)
        banned = '**`{}`**'.format(False)
        if return_bans['status'] == 200:
            banned = '**`{}`**'.format(True)

        embed = Embed.user_information(colour_by_hex, (m_hex, s_hex), (m_string, s_string), user, ctx.author, banned)
        if str(user.id) == '321972163953295361':
            embed = Embed.imperator_information(user, ctx.author)

        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(FlagAdvanced(bot))
