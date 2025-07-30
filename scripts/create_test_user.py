from utils import run_async, get_connection

async def initialize_team(teamname, password, problem_number):
    conn =  await get_connection()
    
    #User_details_2023 init
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS user_details_2023 (
        user_id SERIAL PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL  
        );
    """)



    #rankings_2023 init
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS rankings_2023 (
        team_id INTEGER PRIMARY KEY,
        score INTEGER NOT NULL DEFAULT 0
        );
    """)

    index = 853
    #insert_and_return = f"""
    #    INSERT INTO user_details_2023(user_id, username, password) VALUES ({index}, '{teamname}', '{password}')
    #"""
    insert_and_return = f"""
    INSERT INTO user_details_2023(username, password) 
    VALUES ($1, $2)
    RETURNING user_id;
    """
    team_id = await conn.fetchval(insert_and_return, teamname, password)
    print(team_id)

    print("TEAM ID:", team_id)

    #create_table = f"""
    #    CREATE TABLE team{team_id}(problem_no integer,solved BOOLEAN NOT NULL, attempts integer, answers decimal[], timestamp timestamp);
    #"""
    create_table = f"""
    CREATE TABLE IF NOT EXISTS team{team_id} (
        problem_no INTEGER PRIMARY KEY,
        solved BOOLEAN NOT NULL DEFAULT FALSE,
        attempts INTEGER NOT NULL DEFAULT 0,
        answers DECIMAL[] DEFAULT '{{}}',
        timestamp TIMESTAMP DEFAULT NOW()
    );
    """

    await conn.execute(create_table)
    print(team_id)

    rows = ",".join(f"({i}, FALSE, 0)" for i in range(1, problem_number + 1))
    insert_rows = f"INSERT INTO team{team_id}(problem_no, solved, attempts) VALUES {rows};"
    await conn.execute(insert_rows)
    print(team_id)

    insert_query = f"""
        INSERT INTO team{team_id} (problem_no, solved, attempts) VALUES """ + ', '.join(f"({number}, FALSE, 0)" for number in range(1, problem_number+1)) + ";"
    
    #insert_rankings = f"""INSERT INTO rankings_2023(team_id, score) VALUES (853, 0)"""

    insert_rankings = """
    INSERT INTO rankings_2023 (team_id, score)
    VALUES ($1, 0);
    """
    await conn.execute(insert_rankings, team_id)
    print("rank added")

    #await conn.execute(create_table)
    #await conn.execute(insert_query)
    #await conn.execute(insert_rankings, team_id)
if __name__ == "__main__":
    run_async(initialize_team("tombradyfans", "password", 35))