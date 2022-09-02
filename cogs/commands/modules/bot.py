from p_modules import get
from p_modules.graphical.embeds import Embed
from p_modules.database.main import Database



async def fetch_user_entry(user):
    client = Database.connect_to_database(get.config('mongodb'))
    collection = Database.get_collection(client, 'BoronideUserDB', 'Users')
    return Database.read_entry(collection, '_id', int(user.id))


async def send_dm(member, description, title):
    try:
        embed = Embed.plain(description=description, title=title)
        return await member.send(embed=embed)
    except Exception as e:
        return {'status': 100, 'returnValue': e}