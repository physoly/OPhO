from decimal import Decimal
from utils import get_connection, run_async

with open('../data/problems.txt') as f:
    questions = [(i+1, Decimal(line.rstrip())) for i, line in enumerate(f)]

async def insert_problems():
    conn = await get_connection()
    insert_problem_query = await conn.prepare('''UPDATE problems SET answer=$1 WHERE problem_no=$2 RETURNING problem_no''')
    
    for question_no, answer in questions:
        _ = await insert_problem_query.fetchval(answer, question_no)

run_async(insert_problems())