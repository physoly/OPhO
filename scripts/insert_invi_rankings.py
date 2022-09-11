import csv
from utils import get_connection, run_async

async def execute():
    root = "INSERT INTO invi_scores_2022(team_name,t1, t2, t3, t4, t5, exp, total) VALUES "
    entries = [] 
    with open('opho2022_invi_final.csv', 'r') as csvin:
        for line in csv.reader(csvin):
            team = line[0]
            t1,t2,t3,t4, t5 = line[1], line[2], line[3], line[4], line[5],
            exp = line[7]
            total = line[8]

            entries.append(f"(\'{team}\', {t1}, {t2}, {t3}, {t4}, {t5}, {exp}, {total})")
        query = root + ','.join(entries)
        conn = await get_connection()
        print(query)
        await conn.execute(query)


run_async(execute()) 
