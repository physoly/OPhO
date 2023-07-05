from utils import run_async, get_connection

async def execute():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT user_id FROM user_details_2022')
    
    table_names = ', '.join([f"team{team_id[0]}" for team_id in team_ids])
    # print(table_names)

    query = f"DROP TABLE {table_names}"
    print(query)

    await conn.execute(query)

run_async(execute())
