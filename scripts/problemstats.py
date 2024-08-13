import asyncio
from collections import defaultdict
from utils import get_connection  # Assuming this function provides a database connection

async def gather_problem_stats(conn, problem_count):
    problem_stats = defaultdict(int)

    # Fetch all team IDs
    team_ids = await conn.fetch("SELECT user_id FROM user_details_2024")

    for team_id_record in team_ids:
        team_id = team_id_record['user_id']
        table_name = f"team{team_id}"

        # Query to count solved problems per problem number for this team
        query = f"""
            SELECT problem_no
            FROM {table_name}
            WHERE solved = TRUE;
        """

        # Fetch solved problem numbers for this team
        solved_problems = await conn.fetch(query)

        # Update problem stats with counts
        for record in solved_problems:
            problem_no = record['problem_no']
            problem_stats[problem_no] += 1

    # Ensure all problems are present in the dictionary
    for i in range(1, problem_count + 1):
        if i not in problem_stats:
            problem_stats[i] = 0

    return problem_stats

async def main():
    # Get the database connection
    conn = await get_connection()

    # Define the number of problems (adjust as needed)
    problem_count = 35

    # Collect problem statistics
    problem_stats = await gather_problem_stats(conn, problem_count)

    # Output the stats
    print(f"Stats for each problem: {dict(problem_stats)}")

    # Close the connection if needed (depends on how get_connection is implemented)
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
