from utils import run_async, get_connection

async def initialize_team(teamname, password, problem_number):

    conn =  await get_connection()
    index = 938
    # insert_and_return = f"""
    #     INSERT INTO user_details_2023(user_id, username, password) VALUES ({index}, '{teamname}', '{password}')
    # """
    
    # team_id = await conn.fetchval(insert_and_return)

    # print("TEAM ID:", index)

    create_table = f"""
        CREATE TABLE team{index}(problem_no integer,solved BOOLEAN NOT NULL, attempts integer, answers decimal[], timestamp timestamp);
    """
    insert_query = f"""
        INSERT INTO team{index} (problem_no, solved, attempts) VALUES """ + ', '.join(f"({number}, FALSE, 0)" for number in range(1, problem_number+1)) + ";"
    
    insert_rankings = f"""INSERT INTO rankings_2023(team_id, score) VALUES ({index}, 0)"""
    await conn.execute(create_table)
    await conn.execute(insert_query)
    # await conn.execute(insert_rankings, team_id)

run_async(initialize_team("tombradyfans", "password", 35))