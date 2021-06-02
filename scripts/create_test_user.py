from utils import run_async, get_connection

async def initialize_team(teamname, password, problem_number):
    conn =  await get_connection()
    insert_and_return = f"""
        INSERT INTO user_details_2021(username, password) VALUES ('{teamname}', '{password}') RETURNING user_id
    """
    
    team_id = await conn.fetchval(insert_and_return)

    print("TEAM ID:", team_id)

    create_table = f"""
        CREATE TABLE team{team_id}(problem_no integer references problems,solved BOOLEAN NOT NULL, attempts integer, answers decimal[], timestamp timestamp);
    """
    insert_query = f"""
        INSERT INTO team{team_id} (problem_no, solved, attempts) VALUES """ + ', '.join(f"({number}, FALSE, 0)" for number in range(1, problem_number+1)) + ";"
    
    insert_rankings = f"""INSERT INTO rankings_2021(team_id, problems_solved) VALUES ($1, 0)"""
    await conn.execute(create_table)
    await conn.execute(insert_query)
    await conn.execute(insert_rankings, team_id)

run_async(initialize_team("Epsilon", "IREADMORIN2", 35))