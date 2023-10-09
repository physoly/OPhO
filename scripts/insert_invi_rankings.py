import csv
from utils import get_connection, run_async

async def execute():
    root = "INSERT INTO invi_scores_2023(team_name,t1, t2, t3, exp, total) VALUES "
    entries = [] 
    with open('./scripts/opho2023_invi_final.csv', 'r') as csvin:
        for line in csv.reader(csvin):
            team = line[0]
            t1,t2,t3 = line[1], line[2], line[3]
            exp = line[4]
            total = line[5]

            entries.append(f"(\'{team}\', {t1}, {t2}, {t3}, {exp}, {total})")
        query = root + ','.join(entries)
        conn = await get_connection()
        print(query)
        await conn.execute(query)


run_async(execute()) 
