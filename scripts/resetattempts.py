import asyncio
from utils import get_connection  # Ensure this utility is correctly defined to get your database connection

async def reset_attempts_for_problem(conn, problem_no):
    # Fetch all team IDs
    team_ids = await conn.fetch("SELECT user_id FROM user_details_2024")

    for team_id_record in team_ids:
        team_id = team_id_record['user_id']

        # Fetch the current state of the problem for this team
        query = f"SELECT solved FROM team{team_id} WHERE problem_no=$1"
        problem_data = await conn.fetchrow(query, problem_no)

        # Check if problem data is valid
        if problem_data is not None:
            if problem_data['solved']:
                # Set attempts to 1 if the problem is solved
                await conn.execute(
                    f"UPDATE team{team_id} SET attempts=1 WHERE problem_no=$1",
                    problem_no
                )
                print(f"Team {team_id}: Solved problem {problem_no}. Attempts set to 1.")
            else:
                # Reset attempts to 0 if the problem is not solved
                await conn.execute(
                    f"UPDATE team{team_id} SET attempts=0 WHERE problem_no=$1",
                    problem_no
                )
                print(f"Team {team_id}: Unsolved problem {problem_no}. Attempts reset to 0.")

async def main():
    # Get the database connection
    conn = await get_connection()

    # Specify the problem number to reset
    problem_no = 30

    # Reset attempts for the specified problem
    await reset_attempts_for_problem(conn, problem_no)

    # Close the connection
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
