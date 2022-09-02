from p_modules import get
from p_modules.database.main import Database
from p_modules.utilities.flag import Flag
from p_modules.graphical.embeds import Embed
import json


async def fetch_user_entry(user):
    client = Database.connect_to_database(get.config('mongodb'))
    collection = Database.get_collection(client, 'BoronideUserDB', 'Users')
    return Database.read_entry(collection, '_id', int(user.id))


async def check_user_permissions(ctx, read):
    author_flag = None
    author_has_permissions = False
    if read['status'] == 200:
        author_flag = read['returnValue']['m_flag']
        if 'moderator' in Flag.Get.flag_permissions(author_flag, 'm_flag'):
            author_has_permissions = True

    if author_flag is None or not author_has_permissions:
        return False
    return True


async def database_process(method, package):
    client = Database.connect_to_database(get.config('mongodb'))
    collection = Database.get_collection(client, 'BoronideUserDB', 'Users')
    if method == 'create':
        return Database.create_entry(collection, package)
    elif method == 'delete':
        return Database.delete_entry(collection, package[0], package[1])


async def process_method(ctx, method, user, email):
    read = await fetch_user_entry(user)
    if method == 'create':
        if read['status'] == 200:
            embed = Embed.error(description='||**User <@{}> already has a entry**||', title='User already exists')
            await ctx.respond(embed=embed)
            return {'status': 100}
        post = {"_id": user.id, "email": email, "m_flag": 0x0, "s_flag": 0x1}
        json_format = json.dumps({"_id": user.id, "email": email, "m_flag": 0x0, "s_flag": 0x1})
        description = 'Preview: JSON Format\n```json\n{}\n``` '.format(json_format)
        await database_process(method, post)

        return {'status': 200, 'returnMessage': description}
    if method == 'delete':
        if read['status'] == 100:
            embed = Embed.error(description='||**User <@{}> does not have a entry**||', title='User does not exist')
            await ctx.respond(embed=embed)
            return {'status': 100}

        email = read['returnValue']['email']
        m_flag = read['returnValue']['m_flag']
        s_flag = read['returnValue']['m_flag']
        json_format = json.dumps({"_id": user.id, "email": email, "m_flag": m_flag, "s_flag": s_flag})
        description = "Deleting Entry: ```json\n{}\n```".format(json_format)
        debug = await database_process(method, ('_id', user.id))

        if debug['status'] == 100:
            embed = Embed.error(description='||{}||'.format(debug['returnValue']), title='Error with Command')
            await ctx.respond(embed=embed)

        return {'status': 200, 'returnMessage': description}
