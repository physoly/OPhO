from utils import get_connection, run_async
from decimal import Decimal

problem_no = 6
answer = Decimal(883)

def check_answer(attempt, answer, error=Decimal(0.01)):
    return abs(attempt-answer) < error * answer

def get_attempt_details(answers, answer):
    for i in range(len(answers)):
        if check_answer(attempt=answers[i], answer=answer):
            return i+1, True
    return -1, False

async def execute():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT user_id FROM user_details')

    for team_id in team_ids:
        answers = await conn.fetchval(f'SELECT answers from team{team_id[0]} WHERE problem_no=$1', problem_no)
        
        if answers is not None:
            attempts, is_correct = get_attempt_details(answers, answer)
            if is_correct:
                await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 WHERE problem_no=$2', True, problem_no)
                await conn.execute(f'UPDATE rankings SET problems_solved = problems_solved + 1 WHERE team_id=$1', team_id[0])
                await conn.execute(f'UPDATE team{team_id[0]} SET attempts=$1 where problem_no=$2', attempts, problem_no)
                print("TEAM ID: ", team_id[0], "ATTEMPTS: ", attempts)
run_async(execute())

