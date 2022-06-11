from utils import get_connection, run_async
from decimal import Decimal

problem_no = 4
answer = Decimal(-2)    
answer_list = [Decimal(0.628), Decimal(0.0999), Decimal(2.758), Decimal(0.439)] # in case multiple answers should be accepted
error=Decimal(0.01)
check_solved = True

def check_answer(attempt, answer, error=Decimal(0.01)):
    return abs(attempt-answer) <= abs(error * answer)

def get_attempt_details(answers, answer):
    for i in range(len(answers)):
        if check_answer(attempt=answers[i], answer=answer,error=error):
            return i+1, True
    return -1, False

async def execute():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT user_id FROM user_details_2022')
    #await conn.execute('UPDATE problems SET answer=$2 WHERE problem_no=$1', problem_no, answer)
    #print(f"Problem {problem_no} now has answer {answer}")
    for team_id in team_ids:
        data = await conn.fetchrow(f'SELECT * from team{team_id[0]} WHERE problem_no=$1', problem_no)
        answers = data['answers']
        solved = data['solved']

        if solved and check_solved:
            print('SOLVED TEAM ID: ', team_id[0], "USERNAME: ", await conn.fetchval('SELECT username from user_details_2022 where user_id=$1', team_id[0]))
            continue # here u can see who has solved a question. this is useful in knowing if many teams have gotten some answer
        
        
        if answers is not None:
            attempts, is_correct = get_attempt_details(answers, answer) 
            if is_correct:
                
                if solved:
                    # if alr correct, give credit on whatever attempt they got it
                    print('LLL')
                    await conn.execute(f'UPDATE team{team_id[0]} SET attempts=$1 where problem_no=$2', attempts, problem_no)
                else:
                    #if q hasnt been solved but is correct, set solved, update rankings
                    await conn.execute(f'UPDATE team{team_id[0]} SET solved=$1, attempts=$2 WHERE problem_no=$3', True, attempts, problem_no)
                    await conn.execute(f'UPDATE rankings_2022 SET score=score + 1 WHERE team_id=$1', team_id[0])
                    print("TI", team_id[0])
                print("TEAM ID: ", team_id[0], "ATTEMPTS: ", attempts)

        

        # everything below here clears attempts for a certain q. if ur using this part, comment out above
        #data = await conn.fetchrow(f'SELECT * from team{team_id[0]} WHERE problem_no=$1', problem_no)
        #solved = data['solved']
        #await conn.execute(f'UPDATE team{team_id[0]} ' + "SET answers='{}', attempts=0, solved='f' WHERE problem_no=$1", problem_no)
        #if solved:
            #await conn.execute('UPDATE rankings_2022 SET score=score - 1 WHERE team_id=$1', team_id[0])
            #print("SOLVED: ", team_id[0])
        
       # print(f"Cleared {problem_no} for TEAM ID: {team_id[0]}")
        
run_async(execute())

