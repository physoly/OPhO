from utils import run_async, get_connection
import csv

async def execute():
    conn = await get_connection()
    invi_names = await conn.fetch("select U.username from user_details_2022 U where U.user_id in (select B.team_id from rankings_2022 B where B.score > 76.7)")
    invi_names = [i[0] for i in invi_names]
    print(invi_names)
    with open('../data/2022/opho2022-logins.csv', 'r') as csvin:
       invi_emails=(','.join(line[0] for line in csv.reader(csvin) if line[1] in invi_names))
    print(invi_emails)
    
    

run_async(execute())