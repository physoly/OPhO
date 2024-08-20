import csv
from utils import get_connection, run_async

async def export_to_csv():
    conn = await get_connection()
    
    # Fetch all data from the table (replace 'your_table_name' with your actual table name)
    data = await conn.fetch('SELECT * FROM problems')
    
    # Specify the CSV file path where you want to save the data
    csv_file_path = '/Users/ashmitdutta/OPhO/scripts/data/answers.csv'  # Replace with your actual path
    
    # Write data to the CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write column headers
        if data:
            csv_writer.writerow(data[0].keys())
        
        # Write data rows
        for row in data:
            csv_writer.writerow(row.values())
    
    print(f"Data has been successfully exported to {csv_file_path}")

# Run the export function
run_async(export_to_csv())
