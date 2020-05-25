from utils import get_connection, run_async
from decimal import Decimal

def check_answer(attempt, answer, error=Decimal(0.01)):
    return abs(attempt-answer) < error * answer

async def execute():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT user_id FROM user_details')

    for team_id in team_ids:
        num_solved = await conn.fetchval(f'select count(*) from team{team_id[0]} where solved=$1', True)
        await conn.execute('UPDATE rankings SET problems_solved=$1 WHERE team_id=$2', num_solved, team_id[0])

run_async(execute())
