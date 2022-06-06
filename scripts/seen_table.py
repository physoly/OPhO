from logging import root
from utils import run_async, get_connection

async def execute():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT user_id FROM user_details_2022')
    
    root_query = "INSERT INTO seen(team_id, seen) VALUES "
    values = ', '.join([f"({team_id['user_id']}, 'f')" for team_id in team_ids])

    await conn.execute(root_query + values)

run_async(execute())
