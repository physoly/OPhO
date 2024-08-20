import asyncio
from decimal import Decimal
from math import exp, log, floor
from utils import get_connection  # Assuming this function provides a database connection

# Define the scoring algorithm based on provided code
def get_score(attempts, num_teams_solved, question_num):
    c1 = pow(0.9, attempts - 1)  # accounts for fact that attempts are 012 not 123
    c2 = exp(question_num / 35) + max(5.5 - floor(log(num_teams_solved)), 2)
    return Decimal(c1 * c2)

async def calculate_p34_impact(conn, team_ids):
    problem_no = 34
    impacts = {}

    # Get the number of teams that solved problem 34
    query = f"SELECT COUNT(DISTINCT team_id) FROM log WHERE problem_no = $1 AND attempt_no = 1 AND answer = (SELECT answer FROM problems WHERE problem_no = $2)"
    num_teams_solved = await conn.fetchval(query, problem_no, problem_no)

    for team_id in team_ids:
        # Fetch logs for problem 34 for this team
        query = f"SELECT attempt_no FROM log WHERE team_id = $1 AND problem_no = $2 ORDER BY attempt_no"
        attempts = await conn.fetch(query, team_id, problem_no)

        if not attempts:
            impacts[team_id] = {"impact": 0, "message": "No attempts found"}
            continue

        # Calculate the impact based on the first attempt where the answer was correct
        attempts_count = len(attempts)
        score_from_p34 = get_score(attempts_count, num_teams_solved, problem_no)

        # Optionally: Fetch the current score and see the difference
        query = f"SELECT score FROM rankings_2024 WHERE team_id = $1"
        current_score = await conn.fetchval(query, team_id)

        impacts[team_id] = {
            "score_from_p34": score_from_p34,
            "current_score": current_score,
            "new_score": current_score - Decimal(score_from_p34),
            "impact": current_score - Decimal(score_from_p34)
        }

    return impacts

async def main():
    # Establish database connection
    conn = await get_connection()

    # Teams that solved problem 34
    team_ids = [27, 29, 37, 76, 195, 246, 349, 512, 514, 551, 618, 652, 673, 793, 844, 846, 848, 852, 879, 909, 957]

    # Calculate the impact of problem 34
    impacts = await calculate_p34_impact(conn, team_ids)

    # Display the impact for each team
    for team_id, impact_data in impacts.items():
        print(f"Team {team_id} Impact: {impact_data['impact']} points. Details: {impact_data}")

    # Close the connection
    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
