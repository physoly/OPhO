import csv
from utils import get_connection, run_async

async def execute():
    root = "INSERT INTO rankings_2024(team_id, score) VALUES "   
    entries = [] 
    with open('/Users/ashmitdutta/OPhO/scripts/data/2024_invi_qualifiers.csv', 'r') as csvin:
        reader = csv.reader(csvin)
        next(reader)  # Skip the header row
        for line in reader:
            team_id = line[0]
            score = round(float(line[1]), 3)  # Corrected index to line[1]
            entries.append(f"({team_id}, {score})")
    query = root + ','.join(entries)
    conn = await get_connection()
    print(query)
    await conn.execute(query)

run_async(execute())
