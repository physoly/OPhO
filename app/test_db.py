from .db import AsyncPostgresDB
from .db import create_team_table
import ujson
import asyncio
with open("./config/config.json") as f:
    global_config = ujson.loads(f.read())
test_db = AsyncPostgresDB(dsn=global_config['local_psql_dsn'], user=global_config['local_psql_username'], loop=app.loop)
await test_db.init()

async def to_run():
    await create_team_table(test_db, "test_team", 30)

asyncio.get_event_loop().run_until_complete(to_run())