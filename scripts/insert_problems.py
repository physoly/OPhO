from decimal import Decimal
from utils import get_connection, run_async

import csv


with open('../data/2021/problem-answers.csv') as csvin:
    questions = [(i+1, Decimal(line[0].rstrip())) for i, line in enumerate(csv.reader(csvin))]
# print(questions)

async def insert_problems():
    conn = await get_connection()
    # insert_problem_query = await conn.prepare('''UPDATE problems SET answer=$1 WHERE problem_no=$2 RETURNING problem_no''')
    insert_problem_query = 'INSERT INTO problems(problem_no, answer) VALUES ($1, $2)'
    update_problem_query = 'UPDATE problems SET answer=$2 WHERE problem_no=$1'

    for question_no, answer in questions:
        _ = await conn.execute(update_problem_query, question_no, answer)
        print(f"PR: {question_no} ANSWER: {answer}")

run_async(insert_problems())