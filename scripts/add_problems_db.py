import csv
from utils import get_connection, run_async
from decimal import Decimal, getcontext

async def execute():
    conn = await get_connection()

    # Ensure table exists
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            problem_no INTEGER PRIMARY KEY,
            answer DECIMAL NOT NULL,
            error_bound DECIMAL NOT NULL DEFAULT 0.01
        );
    ''')

    insert_sql = 'INSERT INTO problems(problem_no, answer, error_bound) VALUES ($1, $2, $3)'

    with open('/problems.csv', 'r') as csvin:
        reader = csv.reader(csvin)
        next(reader, None)                  # skip header
        for line in reader:                 # <— everything below must be inside this loop
            if not line or not line[0].strip().isdigit():
                continue

            # now inside the loop:
            problem_no  = int(line[0].strip())
            answer      = Decimal(line[2].strip())
            error_bound = Decimal(line[3].strip())

            await conn.execute(insert_sql, problem_no, answer, error_bound)
            print(f"INSERTED ({problem_no}, {answer}, {error_bound})")

run_async(execute())
