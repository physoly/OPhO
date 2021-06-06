from utils import get_connection, run_async

problem_no = 32

async def execute():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT user_id FROM user_details_2021')

    for team_id in team_ids:
        data = await conn.fetchrow(f'SELECT * from team{team_id[0]} WHERE problem_no=$1', problem_no)
        answers = data['answers']
        solved = data['solved']

        if solved:
            print('SOLVED TEAM ID: ', team_id[0], "USERNAME: ", await conn.fetchval('SELECT username from user_details_2021 where user_id=$1', team_id[0]), "ANSWER: ", answers)

run_async(execute())
