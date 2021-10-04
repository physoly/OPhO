import csv
from utils import get_connection, run_async

async def execute():
    root = "INSERT INTO invi_scores_2021(team_name,t1, t2, t3, t4, th, exp, total) VALUES "
    entries = [] 
    with open('../data/2021/opho2021_invi_res.csv', 'r') as csvin:
        for line in csv.reader(csvin):
            team = line[0]
            t1,t2,t3,t4 = line[3], line[4], line[5], line[6]
            th = line[7]
            exp = line[8]
            total = line[9]

            entries.append(f"(\'{team}\', {t1}, {t2}, {t3}, {t4}, {th}, {exp}, {total})")
        query = root + ','.join(entries)
        conn = await get_connection()
        print(query)
        await conn.execute(query)


run_async(execute()) 
