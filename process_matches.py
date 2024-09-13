import client
import write_csv
import write_excel

def run(league_id):
    game_status = client.get_game_status()
    current_gameweek = game_status['current_event']

    league_data = client.get_league_data(league_id)
    league_entries = league_data['league_entries']
    standings = league_data['standings']

    # Create mapping from league_entry to entry_id
    league_entry_to_entry_id = {entry['id']: entry['entry_id'] for entry in league_entries}
    entry_id_to_name_map = {entry['entry_id']: entry['player_first_name'] for entry in league_entries}

    gameweek_ranks = {entry['entry_id']: [] for entry in league_entries}
    total_scores = {entry['entry_id']: [] for entry in league_entries}

    # Process standings data
    for gameweek in range(1, current_gameweek + 1):
        gameweek_standings = sorted(standings, key=lambda x: x['total'], reverse=True)
        for rank, entry in enumerate(gameweek_standings, 1):
            league_entry = entry['league_entry']
            entry_id = league_entry_to_entry_id[league_entry]
            gameweek_ranks[entry_id].append(rank)
            total_scores[entry_id].append(entry['total'])

    # Calculate total score average difference
    total_score_avg_diff = {entry['entry_id']: [] for entry in league_entries}
    for gw in range(current_gameweek):
        average = sum(scores[gw] for scores in total_scores.values()) / len(league_entries)
        for entry_id in total_scores:
            total_score_avg_diff[entry_id].append(total_scores[entry_id][gw] - average)

    write_csv.league_standing_progression(entry_id_to_name_map, current_gameweek, gameweek_ranks)  
    write_excel.league_standing_progression(entry_id_to_name_map, current_gameweek, gameweek_ranks)
    write_csv.total_score_progression(entry_id_to_name_map, current_gameweek, total_scores)
    write_excel.total_score_progression(entry_id_to_name_map, current_gameweek, total_scores)
    write_csv.total_score_avg_diff_progression(entry_id_to_name_map, current_gameweek, total_score_avg_diff)
    write_excel.total_score_avg_diff_progression(entry_id_to_name_map, current_gameweek, total_score_avg_diff)

    print("CSVs generated for process_matches.")