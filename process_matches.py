import client
import write_csv
import write_excel
import write_google

def run(league_id):
    game_status = client.get_game_status()
    current_gameweek = game_status['current_event']

    league_data = client.get_league_data(league_id)
    league_entries = league_data['league_entries']

    # Create mapping from league_entry to entry_id
    entry_id_to_name_to_team_map = {entry['entry_id']: (entry['player_first_name']+ ' ' + entry['player_last_name'][0], entry['entry_name']) for entry in league_entries}

    gameweek_scores = {entry['entry_id']: [] for entry in league_entries}
    total_scores = {entry['entry_id']: [] for entry in league_entries}

    # Process each entry ID
    for entry_id in gameweek_scores.keys():
        history = client.get_manager_history(entry_id)
        
        if history:
            # Sort the history by event number
            sorted_history = sorted(history, key=lambda x: x['event'])
            
            # Initialize event counter
            current_event = 1
            
            for event in sorted_history:
                # Fill in any missing events with None
                while current_event < event['event']:
                    gameweek_scores[entry_id].append(None)
                    total_scores[entry_id].append(None)
                    current_event += 1
                
                # Append the actual points and total_points
                gameweek_scores[entry_id].append(event['points'])
                total_scores[entry_id].append(event['total_points'])
                current_event += 1


    write_csv.weekly_score(entry_id_to_name_to_team_map, current_gameweek, gameweek_scores) 
    write_google.weekly_score(entry_id_to_name_to_team_map, current_gameweek, gameweek_scores) 
    write_excel.weekly_score(entry_id_to_name_to_team_map, current_gameweek, gameweek_scores)

    write_csv.total_score_progression(entry_id_to_name_to_team_map, current_gameweek, total_scores)
    write_google.total_score_progression(entry_id_to_name_to_team_map, current_gameweek, total_scores)
    write_excel.total_score_progression(entry_id_to_name_to_team_map, current_gameweek, total_scores)


    print("CSVs generated for process_matches.")
    