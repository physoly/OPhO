from utils import get_connection, run_async

problem_no = 34
problem_no_2 = 32

async def execute():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT user_id FROM user_details_2021')

    for team_id in team_ids:
        data = await conn.fetchrow(f'SELECT * from team{team_id[0]} WHERE problem_no=$1', problem_no)
        answers = data['answers']
        solved = data['solved']

        data_2 = await conn.fetchrow(f'SELECT * from team{team_id[0]} WHERE problem_no=$1', problem_no_2)

        answers_2 = data_2['answers']
        solved_2 = data_2['solved']

        if solved and solved_2:
            uname = await conn.fetchval('SELECT username from user_details_2021 where user_id=$1', team_id[0])
            print('TEAM ID: ', team_id[0], "USERNAME: ",uname, "ANSWER q34: ", answers, "ANSWER q32", answers_2)

run_async(execute())
