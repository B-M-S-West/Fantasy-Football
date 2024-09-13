import os
from dotenv import load_dotenv
import write_csv
import write_excel
import process_matches
import process_transfers
import process_point_breakdowns

# Load environment variables from .env file
load_dotenv()

# Get the LEAGUE_ID from environment variables
LEAGUE_ID = int(os.getenv('LEAGUE_ID'))

def main():
    print(f"Starting analysis for league ID: {LEAGUE_ID}")
    
    write_csv.directory_reset()
    write_excel.directory_reset()
    
    print("Processing matches...")
    process_matches.run(LEAGUE_ID)
    
    print("Processing transfers...")
    process_transfers.run(LEAGUE_ID)
    
    print("Processing point breakdowns...")
    process_point_breakdowns.run(LEAGUE_ID)

    print("All processing complete! CSV files have been generated in the 'csv' directory.")

if __name__ == "__main__":
    main()