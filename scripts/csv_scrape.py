import csv
import string
import random
#changes not necessary as of rn

from utils import get_connection, run_async

import collections


REQUIRED_FIELDS = [0,2,3,4,5]
PASSWORD_LENGTH = 12

emails = []

YEAR = 2023

def valid_entry(line):
    for field in REQUIRED_FIELDS:
        if line[field] == '':
            return False
    return True

def string_generator(size, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))

async def delete_first():
    conn = await get_connection()
    delete_details = await conn.prepare(f'''DELETE FROM user_details_2023 WHERE user_id = 1;''')
    delete_rankings = await conn.prepare(f'''DELETE FROM rankings_2023 WHERE user_id = 1;''')

    await conn.execute(delete_details)
    await conn.execute(delete_rankings)


#replace csv names with local dir names
async def execute():
    id_num = 1
    names = []
    conn = await get_connection()
    insert_details_query = await conn.prepare(f'''INSERT INTO user_details_{YEAR}(user_id, username, password) VALUES ($1, $2, $3)''')
    #insert_into_rankings = await conn.prepare(f'''INSERT INTO rankings_{YEAR}(team_id, score) VALUES ($1, 0)''')
    with open('/mnt/c/Users/va648/downloads/vscode/opho/scripts/data/2023/opho2023.csv', 'r') as csvin:
        with open('/mnt/c/Users/va648/downloads/vscode/opho/scripts/data/2023/opho2023-logins.csv', 'w') as csvout:
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

                    user_id = await insert_details_query.fetchval(id_num, uname, password)
                    #team_id = await insert_into_rankings.fetchval(user_id)

                    print(f"INSERTING ({id_num, uname, password}")

                    names.append(uname)
                    emails.append(email)
                    id_num = id_num + 1



run_async(execute())
#run_async(delete_first())

p = [item for item, count in collections.Counter(emails).items() if count > 1]
print(p)
