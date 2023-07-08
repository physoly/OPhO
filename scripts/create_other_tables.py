from utils import run_async, get_connection

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

    if(table == 'user_details'):
        query = f'DROP TABLE user_details_{year}'
        await conn.execute(query)
        print(query)
    else:
        query = f'DROP TABLE rankings_{year}'
        await conn.execute(query)
        print(query)

run_async(execute_user_details(CURRENT_YEAR))
#run_async(execute_rankings(CURRENT_YEAR))
#run_async(clear_ranking_user_details(CURRENT_YEAR, 'user_details'))