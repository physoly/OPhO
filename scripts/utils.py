import asyncio
import asyncpg
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv('.env'))

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))

async def get_connection():
    return await asyncpg.connect(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def run_async(func, loop=asyncio.get_event_loop()):
    loop.run_until_complete(func)