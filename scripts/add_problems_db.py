import csv
from utils import get_connection, run_async
from decimal import Decimal, getcontext

async def execute():
    conn = await get_connection()


    insert_problems = await conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS problems (
            problem_no INTEGER PRIMARY KEY,
            answer DECIMAL NOT NULL,
            error_bound DECIMAL NOT NULL DEFAULT 0.01
        );
        '''
    )

    # Prepare the query for inserting into problems table
    insert_problems_query = await conn.prepare(
        '''INSERT INTO problems(problem_no, answer, error_bound) VALUES ($1, $2, $3)'''
    )

    # Open the CSV file with the problem details
    with open('/problems.csv', 'r') as csvin:
        # Read each line from the CSV
        for line in csv.reader(csvin):
            # Assume columns: [problem_no, answer, error_bound]
            problem_no = int(line[0].strip())
            answer = Decimal(line[1].strip())
            error_bound = Decimal(line[2].strip())

            # Insert the problem details into the database
            await insert_problems_query.fetchval(problem_no, answer, error_bound)
            print(f"INSERTING ({problem_no}, {answer}, {error_bound})")

# Run the execute function asynchronously
run_async(execute())

'''
docker run --rm --network opho-net --env-file .env opho python3 scripts/add_problems_db.py
'''