from app import app
import asyncpg

class AsyncPostgresDB():
    def __init__(self, dsn, user, loop):
        self.dsn = dsn
        self.user = user
        self.loop = loop
        self.pool = None
    
    async def init(self):
        self.pool = await asyncpg.create_pool(
            dsn=self.dsn, 
            user=self.user, 
            command_timeout=60, 
            loop=self.loop
        )
    
    async def execute_job(self, query, *args):
	    # args = list(args)
        con = await self.pool.acquire()
        async with con.transaction():
            await con.execute(query, *args)
        await self.pool.release(con)
    
    async def fetch_row(self, query, *args):
        con = await self.pool.acquire()
        async with con.transaction():
            row = await con.fetchrow(query, *args)
        await self.pool.release()
        return row
    
    async def close(self):
        await self.pool.close()
