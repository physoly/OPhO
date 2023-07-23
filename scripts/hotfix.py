from utils import get_connection, run_async
from decimal import Decimal

#problems to hotfix: 10, 21
problem_no = 19
answer = Decimal(0.000699) # updated answer here
error= Decimal(0.01)
check_solved = True

def check_answer(attempt, answer, error=error):
    return abs(attempt-answer) <= abs(error * answer)

def get_attempt_details(answers, answer):
    for i in range(len(answers)):
        if check_answer(attempt=answers[i], answer=answer,error=error):
            return i+1, True
    return -1, False

async def execute():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT user_id FROM user_details_2023')

    for team_id in team_ids:
        data = await conn.fetchrow(f'SELECT * from team{team_id[0]} WHERE problem_no=$1', problem_no)
        answers = data['answers']
        solved = data['solved']

        #block 1
        #if solved and check_solved:
            #print('SOLVED TEAM ID: ', team_id[0], "USERNAME: ", await conn.fetchval('SELECT username from user_details_2022 where user_id=$1', team_id[0]))

        #block 2
        if answers is not None:
            print(str(team_id[0]), answers)
            # attempts, is_correct = get_attempt_details(answers, answer)
            # if solved:
            #     print(str(team_id[0]) + ' has solved it incorrectly but received points')
            # else:
            #     if is_correct:
            #         print(str(team_id[0]) + ' has solved it correctly but received no points')
            #     else:
            #         print(str(team_id[0]) + ' was flat out wrong')
            #         print(answers)

        #block 3
        # if answers is not None:
        #     attempts, is_correct = get_attempt_details(answers, answer) 
        #     if is_correct:
        #         if not solved: # if correct according to updated answer and not solved, update shit
        #             print(team_id[0], len(answers))
        #             if len(answers) == 1:
        #                 print(team_id[0])
        #                 await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 where problem_no=$2', True, problem_no)
        #                 await conn.execute(f'UPDATE rankings_2023 SET score=score+1 WHERE team_id=$1', team_id[0])
        #             else:
        #                 print(team_id[0])
        #                 await conn.execute(f'UPDATE team{team_id[0]} SET attempts=$1 where problem_no=$2', attempts, problem_no)
        #                 await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 where problem_no=$2', True, problem_no)
        #                 await conn.execute(f'UPDATE rankings_2023 SET score=score+1 WHERE team_id=$1', team_id[0])
        #     else:
        #         if solved:
        #             await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 where problem_no=$2', False, problem_no)
        #             await conn.execute(f'UPDATE rankings_2023 SET score=score-1 WHERE team_id=$1', team_id[0])
        
       
        
run_async(execute())

