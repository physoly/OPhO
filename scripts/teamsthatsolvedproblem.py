import asyncio
from utils import get_connection  # Assuming this function provides a database connection

async def find_teams_that_solved_problem(conn, problem_no):
    teams_that_solved = []

    # Fetch all team IDs
    team_ids = await conn.fetch("SELECT user_id FROM user_details_2024")

    for team_id_record in team_ids:
        team_id = team_id_record['user_id']
        table_name = f"team{team_id}"

        # Query to check if the specific problem was solved by this team
        query = f"""
            SELECT solved
            FROM {table_name}
            WHERE problem_no = $1;
        """

        # Fetch the solved status for the specific problem
        solved_status = await conn.fetchval(query, problem_no)

        # If the problem was solved, add the team ID to the list
        if solved_status:
            teams_that_solved.append(team_id)

    return teams_that_solved

async def main():
    # Get the database connection
    conn = await get_connection()

    # Specify the problem number you're interested in
    problem_no = 34

    # Find all teams that solved the specified problem
    teams_that_solved = await find_teams_that_solved_problem(conn, problem_no)

    # Output the list of teams
    print(f"Teams that solved problem {problem_no}: {teams_that_solved}")

    # Close the connection if needed (depends on how get_connection is implemented)
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
