import csv
from utils import get_connection, run_async

YEAR = 2024

async def execute():
    id_num = 1
    conn = await get_connection()

    # Prepare the query for inserting into user_details_2024
    insert_details_query = await conn.prepare(
        f'''INSERT INTO user_details_{YEAR}(user_id, username, password) VALUES ($1, $2, $3)'''
    )

    # Open the CSV file with the updated user details
    with open('/Users/ashmitdutta/OPhO/scripts/data/details.csv', 'r') as csvin:
        # Read each line from the CSV, starting user_id at 1 and incrementing
        for user_id, line in enumerate(csv.reader(csvin), start=1):
            # Assume columns: [email, username, password]
            email = line[0].strip()  # This is the email, but we're not using it for insertion
            username = line[1].strip().replace(" ", "_")
            password = line[2].strip()

            # Insert the user details into the database
            await insert_details_query.fetchval(user_id, username, password)
            print(f"INSERTING ({user_id}, {username}, {password})")

# Run the execute function asynchronously
run_async(execute())