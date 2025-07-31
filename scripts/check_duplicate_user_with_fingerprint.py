from utils import get_connection, run_async

async def execute(team_id: int, ja3_hash: str):
    conn = await get_connection()
    try:
        #This finds duplicate logins by fingerprint
        duplicates = await conn.fetch(
            """
            SELECT *
              FROM device_fingerprints
             WHERE team_id = $1
               AND ja3_hash = $2
            """,
            team_id,
            ja3_hash
        )

        if duplicates:
            print(f"Found {len(duplicates)} matching fingerprint(s):")
            for row in duplicates:
                print(dict(row))
        else:
            print("No duplicate fingerprints found")

    finally:
        await conn.close()

if __name__ == "__main__":
    TEAM_ID   = 1e9  #Replace with actual team ID
    JA3_HASH  = "" #Replace with actual JA3 hash

    run_async(execute(TEAM_ID, JA3_HASH))

'''
docker run --rm --network opho-net --env-file .env opho python3 scripts/check_duplicate_user_with_fingerprint.py
'''