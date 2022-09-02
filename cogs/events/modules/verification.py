import time

from p_modules import get
from p_modules.graphical.embeds import Embed
from p_modules.database.main import Database
import asyncio


async def fetch_user_entry(user):
    client = Database.connect_to_database(get.config('mongodb'))
    collection = Database.get_collection(client, 'BoronideUserDB', 'Users')
    return Database.read_entry(collection, '_id', int(user.id))


async def create_entry(member):
    client = Database.connect_to_database(get.config('mongodb'))
    collection = Database.get_collection(client, 'BoronideUserDB', 'Users')
    return Database.create_entry(collection, {"_id": member.id, "email": 'no@email.com', "m_flag": 0x0, "s_flag": 0x0})


async def send_dm(member, description, title):
    try:
        embed = Embed.plain(description=description, title=title)
        await member.send(embed=embed)
        return {'status': 200}
    except Exception as e:
        return {'status': 100, 'returnValue': e}


async def verification_status(member):
    fetch_user = await fetch_user_entry(member)
    if fetch_user['status'] == 200:
        if fetch_user['returnValue']['s_flag'] == 1:
            return 0
    return None


async def initiate_kick_timer(member):
    for i in range(get.config('time')):
        await asyncio.sleep(1)
        if i == get.config('time')-1:
            if await verification_status(member) is None:
                return {'status': 100, 'returnMessage': 'User did not verify in time'}
            return {'status': 200, 'returnMessage': 'User verified in time'}
        if await verification_status(member) is not None:
            return {'status': 200, 'returnMessage': 'User verified in time'}


async def start_verification_process(member):
    timer_results = await initiate_kick_timer(member)
    if timer_results['status'] == 200:
        return {'status': 200, 'returnValue': 'Verification Successful'}
    return {'status': 100, 'returnValue': 'Verification Failed'}









