from utils import get_connection, run_async
from decimal import Decimal

problem_no = 33
answer = Decimal(7.14e7)     
error=Decimal(0.01)

def check_answer(attempt, answer, error=Decimal(0.01)):
    return abs(attempt-answer) < error * answer

def get_attempt_details(answers, answer):
    for i in range(len(answers)):
        if check_answer(attempt=answers[i], answer=answer,error=error):
            return i+1, True
    return -1, False

async def execute():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT user_id FROM user_details_2021')
    await conn.execute('UPDATE problems SET answer=$2 WHERE problem_no=$1', problem_no, answer)
    print(f"Problem {problem_no} now has answer {answer}")
    for team_id in team_ids:
        data = await conn.fetchrow(f'SELECT * from team{team_id[0]} WHERE problem_no=$1', problem_no)
        answers = data['answers']
        solved = data['solved']

        if solved:
            print('SOLVED TEAM ID: ', team_id[0], "USERNAME: ", await conn.fetchval('SELECT username from user_details_2021 where user_id=$1', team_id[0]))
            continue
    
        if answers is not None and not solved:
            attempts, is_correct = get_attempt_details(answers, answer)
            if is_correct:
                await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 WHERE problem_no=$2', True, problem_no)
                await conn.execute(f'UPDATE rankings_2021 SET score=score + 1 WHERE team_id=$1', team_id[0])
                await conn.execute(f'UPDATE team{team_id[0]} SET attempts=$1 where problem_no=$2', attempts, problem_no)
                print("TEAM ID: ", team_id[0], "ATTEMPTS: ", attempts)

        


        #data = await conn.fetchrow(f'SELECT * from team{team_id[0]} WHERE problem_no=$1', problem_no)
        #solved = data['solved']
        #await conn.execute(f'UPDATE team{team_id[0]} ' + "SET answers='{}', attempts=0, solved='f' WHERE problem_no=$1", problem_no)
        #if solved:
            #await conn.execute('UPDATE rankings SET problems_solved=problems_solved - 1 WHERE team_id=$1', team_id[0])
            #print("SOLVED: ", team_id[0])
        
       # print(f"Cleared {problem_no} for TEAM ID: {team_id[0]}")
        
run_async(execute())

