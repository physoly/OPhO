from logging import root
from utils import run_async, get_connection

async def execute():
    conn = await get_connection()
    #team_ids = await conn.fetch('SELECT user_id FROM user_details_2023 WHERE user_id')
    team_ids = [[2]]
    # > 397
    
    for team_id in team_ids:
        root_query = f"INSERT INTO seen(team_id, seen) VALUES ({team_id[0]}, True)"
        await conn.execute(root_query)

run_async(execute())
