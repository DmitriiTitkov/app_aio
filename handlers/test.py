import asyncio
import asyncpg
from model.database import Database


async def run():
    db = await Database.create("../config/database.json")
    print(await db.users.get_all_users())
    print(dir(db.pool))

loop = asyncio.get_event_loop()
loop.run_until_complete(run())


# data = json.load(open('config/database.json'))
