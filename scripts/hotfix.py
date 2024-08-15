from utils import get_connection, run_async
from decimal import Decimal

problem_no = 24
answer = Decimal(266) # updated answer here
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
    team_ids = await conn.fetch('SELECT user_id FROM user_details_2024')
    incorrect = []
    correct = [] # teams that answered p1 on the first try

    for team_id in team_ids:
        data = await conn.fetchrow(f'SELECT * from team{team_id[0]} WHERE problem_no=$1', problem_no)
        answers = data['answers']
        solved = data['solved']

        # block 1
        # if answers is not None:
        #     attempts, is_correct = get_attempt_details(answers, answer)
        #     if is_correct:
        #         print(team_id[0])
        #         print(answers)
        #         print('')

        # block 2
        # logic for problem 1 fix
        # if answers is not None:
        #     list = []
        #     list.append(answers[0]) # append the first answer to a list which we can throw into the function below
        #     attempts, is_correct = get_attempt_details(list, answer)
        #     if is_correct:
        #         print(str(team_id[0]) + ' has solved it correctly on their first try')
        #         await conn.execute(f'UPDATE team{team_id[0]} SET attempts=$1 where problem_no=$2', 3, problem_no)
        #         await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 where problem_no=$2', True, problem_no)
        #         if not solved: # if the user gave up after first try
        #             await conn.execute(f'UPDATE rankings_2023 SET score=score+1 WHERE team_id=$1', team_id[0])
        #     else:
        #         print(str(team_id[0]) + ' has solved it incorrectly on their first try')
        #         await conn.execute(f'UPDATE team{team_id[0]} SET attempts=$1 where problem_no=$2', 3, problem_no)
        #         await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 where problem_no=$2', False, problem_no)
        #         if solved: # if the user
        #             await conn.execute(f'UPDATE rankings_2023 SET score=score-1 WHERE team_id=$1', team_id[0])

        # block 3 for initializing/updating single answer problems e.g. 1, 27
        # if answers is not None:
        #     if solved and len(answers) >1:
        #         print(team_id[0])
        #         await conn.execute(f'UPDATE team{team_id[0]} SET attempts=$1 where problem_no=$2', 3, problem_no)
        #         await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 where problem_no=$2', False, problem_no)
        #         await conn.execute(f'UPDATE rankings_2023 SET score=score-1 WHERE team_id=$1', team_id[0])
        #     if not solved:
        #         print(team_id[0])
        #         await conn.execute(f'UPDATE team{team_id[0]} SET attempts=$1 where problem_no=$2', 3, problem_no)

        # block 4
        if answers is not None:
            attempts, is_correct = get_attempt_details(answers, answer) 
            if is_correct:
                if not solved: # if correct according to updated answer and not solved, update shit
                    if len(answers) == 1:
                        print(team_id[0])
                        await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 where problem_no=$2', True, problem_no)
                        await conn.execute(f'UPDATE rankings_2024 SET score=score+1 WHERE team_id=$1', team_id[0])
                    else:
                        print(team_id[0])
                        await conn.execute(f'UPDATE team{team_id[0]} SET attempts=$1 where problem_no=$2', attempts, problem_no)
                        await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 where problem_no=$2', True, problem_no)
                        await conn.execute(f'UPDATE rankings_2024 SET score=score+1 WHERE team_id=$1', team_id[0])
                else: # if team got it right first try (but it was counted wrong) then got it right (according to incorrect answer key) on the second try, just update that team's attempts
                    await conn.execute(f'UPDATE team{team_id[0]} SET attempts=$1 where problem_no=$2', attempts, problem_no)
                    print('updated team', team_id[0])
            else:
                if solved:
                    await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 where problem_no=$2', False, problem_no)
                    await conn.execute(f'UPDATE rankings_2024 SET score=score-1 WHERE team_id=$1', team_id[0])
                    print('removed points from ' + str(team_id[0]))

        # block 5 for voiding p6 for all competitors
        # await conn.execute(f'UPDATE team{team_id[0]} SET attempts=$1 where problem_no=$2', 3, problem_no) # lock teams out
        # print('updated team attempts for team ', team_id[0])
        # await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1 where problem_no=$2', False, problem_no)
        # print('updated solved status for team ', team_id[0])
        # if solved:
        #     await conn.execute(f'UPDATE rankings_2023 SET score=score-1 WHERE team_id=$1', team_id[0])
        #     print('removed points for team ', team_id[0])

        
       
        
run_async(execute())

