import csv
import string
import random

from utils import get_connection, run_async

import collections


REQUIRED_FIELDS = [0,2,3,4,5]
PASSWORD_LENGTH = 12

emails = []

YEAR = 2022

def valid_entry(line):
    for field in REQUIRED_FIELDS:
        if line[field] == '':
            return False
    return True

def string_generator(size, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

async def execute():
    names = []
    conn = await get_connection()
    insert_details_query = await conn.prepare(f'''INSERT INTO user_details_{YEAR}(username, password) VALUES ($1, $2) RETURNING user_id''')
    insert_into_rankings = await conn.prepare(f'''INSERT INTO rankings_{YEAR}(team_id, score) VALUES ($1, 0) RETURNING team_id''')
    with open('../data/2022/opho2022-late.csv', 'r') as csvin:
        with open('../data/2022/opho2022-late-logins.csv', 'w') as csvout:
            writer = csv.writer(csvout)

            for line in csv.reader(csvin):
                if valid_entry(line):
                    uname = line[2].strip().replace(" ", "_")
                    email = line[5].strip()

                    if len(uname) > 25:
                        uname=uname[:26]
                    
                    idx = 1
                    while uname in names:
                        uname = uname + str(idx)
                        idx = idx + 1

                    password = string_generator(PASSWORD_LENGTH)

                    writer.writerow([email, uname, password])

                    user_id = await insert_details_query.fetchval(uname, password)
                    team_id = await insert_into_rankings.fetchval(user_id)

                    print(f"INSERTING ({uname, password}")

                    names.append(uname)
                    emails.append(email)



run_async(execute())

p = [item for item, count in collections.Counter(emails).items() if count > 1]
print(p)
