from p_modules import get
from p_modules.database.main import Database
from p_modules.utilities.flag import Flag
from p_modules.graphical.embeds import Embed
import ast


async def fetch_user_entry(user):
    client = Database.connect_to_database(get.config('mongodb'))
    collection = Database.get_collection(client, 'BoronideUserDB', 'Users')
    return Database.read_entry(collection, '_id', int(user.id))


async def fetch_bans(user):
    client = Database.connect_to_database(get.config('mongodb'))
    collection = Database.get_collection(client, 'BoronideUserDB', 'Bans')
    return Database.read_entry(collection, '_id', int(user.id))


async def check_user_permissions(ctx, read):
    author_flag = None
    author_has_permissions = False
    if read['status'] == 200:
        author_flag = read['returnValue']['s_flag']
        if 'imperator' in Flag.Get.flag_permissions(author_flag, 's_flag'):
            author_has_permissions = True

    if author_flag is None or not author_has_permissions:
        return False
    return True


async def process_type(validate_type, flag):
    if validate_type['returnValue'] == 'string':
        get_hex = None
        if flag[:1] == '[':
            get_hex = Flag.Get.get_hex(ast.literal_eval(flag), flag_type)
        elif flag[:1] != '[':
            get_hex = Flag.Get.get_hex(flag, flag_type)

        if get_hex is None:
            return {'status': 100, 'returnValue': 'Error occurred with Flag'}
        if get_hex['status'] == 100:
            return {'status': 100, 'returnValue': get_hex['returnValue']}

        return {'status': 200, 'returnValue': get_hex['returnValue']}
    return {'status': 0}


async def process_by_method(method, ctx, user_flag, flag, flag_type, user):
    flag_calculation = None
    text = None
    if method == 'add':
        flag_calculation = Flag.Get.add_flag_calculation(user_flag, flag, flag_type)
        text = 'to'
    elif method == 'sub':
        flag_calculation = Flag.Get.sub_flag_calculation(user_flag, flag, flag_type)
        text = 'from'

    if flag_calculation['status'] == 100:
        description = '||**`{}`**||'.format(flag_calculation['returnMessage'])
        embed = Embed.error(description=description, title='Invalid Operation')
        return await ctx.respond(embed=embed)

    if flag_calculation['status'] == 200:
        description = '{}\n{} <@{}>'.format(flag_calculation['returnMessage'][0], text, user.id)
        embed = Embed.plain(description=description, title='Successful')
        await ctx.respond(embed=embed)

    if flag_calculation['status'] == 201:
        description = '{}'.format('\n'.join(flag_calculation['returnMessage']))
        embed = Embed.info(description=description, title='Semi-Successful')
        await ctx.respond(embed=embed)

    return flag_calculation['returnValue']


async def manipulate_flags(flag_type, flag, user):
    client = Database.connect_to_database(get.config('mongodb'))
    collection = Database.get_collection(client, 'BoronideUserDB', 'Users')
    return Database.update_entry(collection, '_id', int(user.id), {flag_type: flag})
