from utils import run_async, get_connection

async def execute():    
    conn = await get_connection()
    

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS user_details_2024 (
           team_id INTEGER NOT NULL PRIMARY KEY,
           score INTEGER NOT NULL DEFAULT 0
        );
    """)

    
    #team_ids = await conn.fetch('SELECT team_id FROM user_details_2024')
    #print(team_ids)
    
    #table_names = ', '.join([f"team{team_id[0]}" for team_id in team_ids])
    #print(table_names)

    #query = f"DROP TABLE {table_names}"
    #print(query)

    #await conn.execute(query)

    #manual
    # team_ids = [172, 201, 207, 269, 270, 289, 341, 351, 371, 430, 481, 57, 58, 584, 597, 611, 614, 676, 679, 704, 727, 742, 814, 815, 854, 868, 878, 891, 906, 907, 921, 922]
    # table_names = ', '.join([f"team{team_id}" for team_id in team_ids])
    
    # query = f"DROP TABLE {table_names}"
    
    # await conn.execute(query)

run_async(execute())

async def drop_team_table(team_id: int):
    conn = await get_connection()
    await conn.execute(f"DROP TABLE IF EXISTS team{team_id};")
    print(f"Dropped table team{team_id}")

if __name__ == "__main__":
    run_async(execute())
    n = 1e9
    for i in range(1, n):
        run_async(drop_team_table(i))
    run_async(drop_team_table(500))


'''
docker run --rm --network opho-net --env-file .env opho python3 scripts/clear_team_tables.py
'''
