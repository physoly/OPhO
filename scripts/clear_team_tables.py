from utils import run_async, get_connection

async def execute():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT user_id FROM user_details_2023')
    print(team_ids)
    
    table_names = ', '.join([f"team{team_id[0]}" for team_id in team_ids])
    print(table_names)

    query = f"DROP TABLE {table_names}"
    print(query)

    await conn.execute(query)

    #manual
    # team_ids = [172, 201, 207, 269, 270, 289, 341, 351, 371, 430, 481, 57, 58, 584, 597, 611, 614, 676, 679, 704, 727, 742, 814, 815, 854, 868, 878, 891, 906, 907, 921, 922]
    # table_names = ', '.join([f"team{team_id}" for team_id in team_ids])
    
    # query = f"DROP TABLE {table_names}"
    
    # await conn.execute(query)

run_async(execute())
