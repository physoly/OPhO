from utils import get_connection, run_async
from math import exp, log, floor

time_factor = False
total_problems = 35

def get_score(attempts, num_teams_solved, question_num, day_solved=0):
    c1 = pow(0.9, attempts + day_solved - 1) # accounts for fact that attempts are 012 not 123
    c2 = exp(question_num/35) + max(5.5 - floor(log(num_teams_solved)), 2)
    return c1 * c2

async def execute():
    conn = await get_connection()
    team_ids = [team_id[0] for team_id in await conn.fetch('SELECT user_id from user_details_2023')]

    all_team_stats = {}
    scores = {}
    solve_stats = {}
    
    for team_id in team_ids:
        all_team_stats[team_id] = await get_team_stats(conn, team_id)
        scores[team_id] = 0
        print(f"Fetched stats for team {team_id}")
        
    for problem_no in range(1, total_problems):
        solve_stats[problem_no] = get_num_solved(conn, all_team_stats, problem_no)
    
    print(solve_stats)
    
    for team_id, data in all_team_stats.items():
        for problem in data:
            if problem['solved']:
                problem_no = problem['problem_no']
                num_solved = solve_stats[problem_no]
                # day_number = problem['timestamp'].day - 25
                num_attempts = problem['attempts']

                # print("DAY NUMBER: ", day_number)
                raw_score = get_score(attempts=num_attempts,num_teams_solved=num_solved, question_num=problem_no)
                scores[team_id] = scores[team_id] + round(raw_score, 3)

    sorted_scores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    
    query = await conn.prepare(f'SELECT username from user_details_2023 where user_id=$1')

    with open('/mnt/c/Users/va648/downloads/vscode/opho/scripts/data/2023/final_rankings.csv', 'a') as f:
        count = 1
        for team_id, score in sorted_scores:
            teamname = await query.fetchval(team_id)
            f.write(f'{count},{teamname},{team_id},{score}\n')
            count = count + 1

async def get_team_stats(conn, team_id):
    query = await conn.prepare(f'SELECT * from team{team_id}')
    return await query.fetch()

def get_num_solved(conn, all_team_stats, question_no):
    count = 0
    for team_id, data in all_team_stats.items():
        for problem in data:
            if problem['problem_no'] == question_no and problem['solved']:
                count = count + 1
    return count
run_async(execute())