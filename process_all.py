import write_csv
import process_matches
import process_transfers
import process_point_breakdowns

# Set your league ID here
LEAGUE_ID = 70382

def main():
    print(f"Starting analysis for league ID: {LEAGUE_ID}")
    
    write_csv.directory_reset()
    
    print("Processing matches...")
    process_matches.run(LEAGUE_ID)
    
    print("Processing transfers...")
    process_transfers.run(LEAGUE_ID)
    
    print("Processing point breakdowns...")
    process_point_breakdowns.run(LEAGUE_ID)

    print("All processing complete! CSV files have been generated in the 'csv' directory.")

if __name__ == "__main__":
    main()