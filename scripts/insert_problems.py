from decimal import Decimal
from utils import get_connection, run_async

import csv


with open('../data/2022/problem-answers.csv') as csvin:
    questions = [(i+1, Decimal(line[0].rstrip()),Decimal(line[1].rstrip())) for i, line in enumerate(csv.reader(csvin))]
# print(questions)

async def insert_problems():
    conn = await get_connection()
    insert_problem_query = 'INSERT INTO problems(problem_no, answer,error_bound) VALUES ($1, $2,$3)'

    for question_no, answer, error in questions:
       # _ = await conn.execute(insert_problem_query, question_no, answer, error)
        print(f"PR: {question_no} ANSWER: {answer} ERROR bound {error}")

run_async(insert_problems())