import csv
from utils import get_connection, run_async

async def execute():
    root = "INSERT INTO final_rankings(team_id, score) VALUES "   
    entries = [] 
    with open('../data/rankings.csv', 'r') as csvin:
        for line in csv.reader(csvin):
            team_id = line[2]
            score = round(float(line[3]), 3)
            entries.append(f"({team_id}, {score})")
    query = root + ','.join(entries)
    conn = await get_connection()
    await conn.execute(query)
run_async(execute())