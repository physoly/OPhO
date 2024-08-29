import asyncio
from utils import get_connection, run_async
from math import exp, log, floor

total_problems = 36  # make it one more than the actual number of problems

def get_score(attempts, num_teams_solved, question_num):
    c1 = pow(0.9, attempts - 1)  # accounts for fact that attempts are 012 not 123
    c2 = exp(question_num / 35) + max(5.5 - floor(log(num_teams_solved)), 2)
    return c1 * c2

async def calculate_team_score(conn, team_id):
    # Fetch the team stats
    data = await get_team_stats(conn, team_id)
    
    if not data:
        print(f"No data found for team {team_id}.")
        return None
    
    solve_stats = {}
    scores = 0

    # Calculate the number of teams that solved each problem
    for problem_no in range(1, total_problems):
        solve_stats[problem_no] = get_num_solved(conn, {team_id: data}, problem_no)

    # Calculate the score for this team
    for problem in data:
        if problem['solved']:
            problem_no = problem['problem_no']
            num_solved = solve_stats[problem_no]
            day_number = problem['timestamp'].day - 25
            num_attempts = problem['attempts']

            print(f"Problem: {problem_no}, Day Number: {day_number}, Attempts: {num_attempts}")
            raw_score = get_score(attempts=num_attempts, num_teams_solved=num_solved, question_num=problem_no)
            scores += round(raw_score, 3)

    print(f"Score for team {team_id}: {scores}")
    return scores

async def get_team_stats(conn, team_id):
    query = await conn.prepare(f'SELECT * from team{team_id}')
    return await query.fetch()

def get_num_solved(conn, all_team_stats, question_no):
    count = 0
    for team_id, data in all_team_stats.items():
        for problem in data:
            if problem['problem_no'] == question_no and problem['solved']:
                count += 1
    return count

async def main():
    # Get the database connection
    conn = await get_connection()

    # Specify the team_id you want to calculate the score for
    team_id = 396  # Replace with the actual team_id you want to check

    # Calculate and print the team's score
    await calculate_team_score(conn, team_id)

    # Close the connection if needed (depends on how get_connection is implemented)
    await conn.close()

if __name__ == "__main__":
    run_async(main())
