import asyncpg
import ssl

class AsyncPostgresDB():
    def __init__(self, dsn, user, loop):
        self.dsn = dsn
        self.user = user
        self.loop = loop
        self.pool = None
    
    async def init(self):
        ssl_object = ssl.create_default_context(capath=r"./config/cert.pem")
        ssl_object.check_hostname = False
        ssl_object.verify_mode = ssl.CERT_NONE
        
        self.pool = await asyncpg.create_pool(
            dsn=self.dsn, 
            #ssl=ssl_object,
            user=self.user, 
            command_timeout=60, 
            loop=self.loop
        )
    
    async def execute_job(self, query, *args):
        con = await self.pool.acquire()
        async with con.transaction():
            await con.execute(query, *args)
        await self.pool.release(con)
    
    async def fetchrow(self, query, *args):
        con = await self.pool.acquire()
        async with con.transaction():
            row = await con.fetchrow(query, *args)
        await self.pool.release(con)
        return row
    
    async def fetchval(self, query, *args):
        con = await self.pool.acquire()
        async with con.transaction():
            value = await con.fetchval(query, *args)
        await self.pool.release(con)
        return value

    async def fetchall(self, query, *args):
        con = await self.pool.acquire()
        async with con.transaction():
            values = await con.fetch(query, *args)
        await self.pool.release(con)
        return values
    
    async def close(self):
        await self.pool.close()


async def initialize_db(conn, admin_list):
    create_user_table = """
       CREATE TABLE user_details(user_id serial PRIMARY KEY,username VARCHAR (35) UNIQUE NOT NULL, password VARCHAR (35) NOT NULL);
    """

    create_contestant_table = """
        CREATE TABLE contestants (user_id integer REFERENCES user_details, team_name VARCHAR (9) UNIQUE NOT NULL);
    """

    create_admin_table = """
        CREATE TABLE admins(username VARCHAR (35) UNIQUE NOT NULL);
    """

    admin_insert = """
        INSERT INTO admins(username) VALUES
    """ + ', '.join([f"('{uname}')" for uname in admin_list])

    await conn.execute(create_user_table)
    await conn.execute(create_contestant_table)
    await conn.execute(create_admin_table)
    await conn.execute(admin_insert)

async def create_team_table(db, name, problem_number):
    create_table = f"""
        CREATE TABLE {name}(problem_no integer PRIMARY KEY,solved BOOLEAN NOT NULL, attempts_left integer, answers decimal[]);
    """
    insert_query = f"""
        INSERT INTO {name} (problem_no, solved, attempts_left) VALUES """ + ', '.join(f"({number}, FALSE, 3)" for number in range(1, problem_number+1)) + ";"
    
    await db.execute_job(create_table)
    await db.execute_job(insert_query)

async def create_problem_table(db, contest_name):
    query = f"""
        CREATE TABLE {contest_name}_problems(question_no integer, answer decimal);
    """

    await db.execute_job(query)