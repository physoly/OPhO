from app.db import initialize_db
import asyncpg
import asyncio
import ujson

db_name = "testdb"

print(f"Script to initialize database for OPhO portal. Target database: {db_name}")
print("Only run this script on an empty database!")
resp = input("WARNING! Initialization could cause some data to be overriten. Are you sure you want to continue? [y/n]")

async def do_init():
    conn = await asyncpg.connect(f'')
    await initialize_db(
        conn=conn, 
        admin_list=["Qcumber","Lolman","Epsilon"]
    )

if resp=='y' or resp=='Y':
    asyncio.get_event_loop().run_until_complete(do_init())