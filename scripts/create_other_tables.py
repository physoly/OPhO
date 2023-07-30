from utils import run_async, get_connection
import csv

CURRENT_YEAR = 2023

#might be a problem with the password constraint type?
async def execute_user_details(year):
    conn = await get_connection()
    create_user_details_table = f'''
    CREATE TABLE user_details_{year}(user_id integer, username text, password text);
    '''
    await conn.execute(create_user_details_table)

    print(f'CREATING USER TABLE FOR {year}')

async def execute_rankings(year):
    conn = await get_connection()
    create_rankings_table = f'''
    CREATE TABLE rankings_2023(team_id integer, score decimal);
    '''
    await conn.execute(create_rankings_table)

    print(f'CREATING RANKINGS TABLE FOR {year}')

#oops
async def clear_ranking_user_details(year, table):
    conn = await get_connection()


    query = f'DROP TABLE user_details_{year}'
    await conn.execute(query)
    print(query)
 
    query = f'DROP TABLE rankings_{year}'
    await conn.execute(query)
    print(query)

async def fix_rankings():
    conn = await get_connection()
    
    insert_query = f"""
        INSERT INTO rankings_2023 (team_id, score) VALUES """ + ', '.join(f"({number}, 0)" for number in range(2, 938)) + ";"
    await conn.execute(insert_query)

async def update_user_details():
    id_num = 1
    conn = await get_connection()

    insert_details_query = await conn.prepare(f'''INSERT INTO user_details_2023(user_id, username, password) VALUES ($1, $2, $3)''')
    with open('/mnt/c/Users/va648/downloads/vscode/opho/scripts/data/2023/opho2023-updated-logins.csv', 'r') as csvin:

        for line in csv.reader(csvin):

            uname = line[1]
            password = line[2]

            user_id = await insert_details_query.fetchval(id_num, uname, password)
            print(f"INSERTING ({id_num, uname, password}")

            id_num = id_num + 1


def check_duplicates():
    list_names = []
    with open('/mnt/c/Users/va648/downloads/vscode/opho/scripts/data/2023/opho2023-updated-logins.csv', 'r') as csvin:

        for line in csv.reader(csvin):
            uname = line[0]
            if(uname in list_names):
                print(uname + ' ' + line[1])
            else:
                list_names.append(uname)

    print(len(list_names))

async def convert_log():
    conn = await get_connection()
    team_ids = await conn.fetch('SELECT team_id FROM log')

    for team_id in team_ids:
        data = await conn.fetchrow(f'SELECT * from log WHERE team_id=$1', team_id)
        print(data)



# run_async(clear_ranking_user_details(CURRENT_YEAR))
# run_async(execute_user_details(CURRENT_YEAR))
# run_async(execute_rankings(CURRENT_YEAR))
#run_async(fix_rankings())
#run_async(update_user_details())
# check_duplicates()
run_async(convert_log())

#manually set the table primary keys by doing ALTER TABLE tablename ADD PRIMARY KEY (columname)