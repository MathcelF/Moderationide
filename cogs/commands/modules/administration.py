from p_modules import get
from p_modules.database.main import Database
from p_modules.utilities.flag import Flag
from p_modules.graphical.embeds import Embed
import json


async def fetch_user_entry(user):
    client = Database.connect_to_database(get.config('mongodb'))
    collection = Database.get_collection(client, 'BoronideUserDB', 'Users')
    return Database.read_entry(collection, '_id', int(user.id))


async def check_ban(user):
    client = Database.connect_to_database(get.config('mongodb'))
    collection = Database.get_collection(client, 'BoronideUserDB', 'Bans')
    read_entry = Database.read_entry(collection, '_id', int(user.id))
    if read_entry['status'] == 200:
        return None
    return 0


async def check_permissions(ctx):
    read = await moderation_module.fetch_user_entry(ctx.author)
    if not await moderation_module.check_user_permissions(ctx, read):
        return None
    return 0
