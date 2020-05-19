import csv
import string
import random
import asyncio
import asyncpg

loop = asyncio.get_event_loop()

REQUIRED_FIELDS = [0,1,2,3,4,9,10,11]
PASSWORD_LENGTH = 12



def valid_entry(line):
    for field in REQUIRED_FIELDS:
        if line[field] == '':
            return False
    return True

def string_generator(size, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




async def execute():
    names = []
    conn = await asyncpg.connect('')
    insert_details_query = await conn.prepare('''INSERT INTO user_details(username, password) VALUES ($1, $2) RETURNING user_id''')
    insert_into_rankings = await conn.prepare('''INSERT INTO rankings(team_id, problems_solved) VALUES ($1, 0) RETURNING team_id''')
    with open('opho.csv', 'r') as csvin:
        with open('out.csv', 'w') as csvout:
            writer = csv.writer(csvout)

            for line in csv.reader(csvin):
                if valid_entry(line):
                    uname = line[9].strip().replace(" ", "_")

                    if len(uname) > 25:
                        uname=uname[:26]
                    
                    idx = 1
                    while uname in names:
                        uname = uname + str(idx)
                        idx = idx + 1

                    password = string_generator(PASSWORD_LENGTH)

                    writer.writerow(line + [uname, password])

                    user_id = await insert_details_query.fetchval(uname, password)
                    team_id = await insert_into_rankings.fetchval(user_id)

                    names.append(uname)

loop.run_until_complete(execute())