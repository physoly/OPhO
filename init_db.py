from app.db import initialize_db, AsyncPostgresDB
from app.config import Config
import asyncpg
import asyncio
import ujson

db_name = "opho"

print(f"Script to initialize database for OPhO portal. Target database: {db_name}")
print("Only run this script on an empty database!")
resp = input("WARNING! Initialization could cause some data to be overriten. Are you sure you want to continue? [y/n]")

async def do_init():
    db = AsyncPostgresDB(
        user=Config.DB_USERNAME,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        db_name=Config.DB_NAME,
        loop=asyncio.get_event_loop()
    )

    await db.init()
    
    await initialize_db(
        conn=db, 
        admin_list=["Qcumber","Lolman","Epsilon"]
    )

if resp=='y' or resp=='Y':
    asyncio.get_event_loop().run_until_complete(do_init())