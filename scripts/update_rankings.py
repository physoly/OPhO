from utils import get_connection, run_async
from decimal import Decimal
import csv

def check_answer(attempt, answer, error=Decimal(0.01)):
    return abs(attempt-answer) < error * answer

async def execute():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT user_id FROM user_details_2023')

    with open('../data/2023/final_rankings.csv', 'r') as csvin:
        for line in csv.reader(csvin):
            print(line)
            uname = line[1]
            id = int(line[2])
            score = round(Decimal(line[3]),2)

            await conn.execute('UPDATE rankings_2023 SET score=$1 WHERE team_id=$2', score, id)

run_async(execute())
