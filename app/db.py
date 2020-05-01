import asyncpg

class AsyncPostgresDB():
    def __init__(self,user,password,host,port,db_name,loop):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.loop = loop
    
    async def init(self):        
        self.pool = await asyncpg.create_pool(
            user=self.user, 
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db_name,
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

    create_admin_table = """
        CREATE TABLE admins(username VARCHAR (35) UNIQUE NOT NULL);
    """

    admin_insert = """
        INSERT INTO admins(username) VALUES
    """ + ', '.join([f"('{uname}')" for uname in admin_list])

    create_problem_table = """
        CREATE TABLE problems(question_no integer, answer decimal);
    """

    create_rankings_table = """
        CREATE TABLE rankings(team_id integer, problems_solved integer);
    """
    await conn.execute_job(create_user_table)
    await conn.execute_job(create_admin_table)
    await conn.execute_job(admin_insert)
    await conn.execute_job(create_problem_table)

async def initialize_team(db, teamname, password, problem_number):
    insert_and_return = f"""
        INSERT INTO user_details(username, password) VALUES ('{teamname}', '{password}') RETURNING user_id
    """
    
    team_id = await db.fetchval(insert_and_return)

    print("TEAM ID:", team_id)

    create_table = f"""
        CREATE TABLE team{team_id}(problem_no integer references problems,solved BOOLEAN NOT NULL, attempts integer, answers decimal[], timestamp timestamp);
    """
    insert_query = f"""
        INSERT INTO team{team_id} (problem_no, solved, attempts) VALUES """ + ', '.join(f"({number}, FALSE, 0)" for number in range(1, problem_number+1)) + ";"
    
    await db.execute_job(create_table)
    await db.execute_job(insert_query)

async def create_problem_table(db, contest_name):
    query = f"""
        CREATE TABLE {contest_name}_problems(question_no integer, answer decimal);
    """

    await db.execute_job(query)