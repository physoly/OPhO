import csv

from utils import get_connection, run_async

# Team,1,2,3,4,5,6,7,8,9,10,,Total,Rank,Filter Rows to Merge

async def execute():
    conn = await get_connection()
    root = 'INSERT INTO invi_scores(teamname, pr_1, pr_2, pr_3, pr_4, pr_5, pr_6, pr_7, pr_8, pr_9, pr_10, total_score, rank) VALUES '
    entries = []
    with open("../data/opho_invi20.csv", "r") as csvin:
        for line in csv.reader(csvin):
            vals = list(filter(None,line[:-1]))
            vals[0] = "'" + vals[0] + "'"
            entries.append("(" + ','.join(vals) + ")")
    query = root + ','.join(entries)
    print(query)
    await conn.execute(root + ','.join(entries))

run_async(execute())
"""
CREATE TABLE invi_scores(teamname VARCHAR (35), pr_1 decimal, pr_2 decimal, pr_3 decimal, pr_4 decimal, pr_5 decimal, pr_6 decimal, pr_7 decimal, pr_8 decimal, pr_9 decimal, pr_10 decimal, total_score decimal);
"""
