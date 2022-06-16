import csv
from utils import get_connection, run_async

async def execute():
    root = "INSERT INTO rankings_2022(team_id, score) VALUES "   
    entries = [] 
    with open('../data/2022/rankings.csv', 'r') as csvin:
        for line in csv.reader(csvin):
            team_id = line[0]
            score = round(float(line[2]), 3)
            entries.append(f"({team_id}, {score})")
    query = root + ','.join(entries)
    conn = await get_connection()
    print(query)
    await conn.execute(query)
run_async(execute()) 
