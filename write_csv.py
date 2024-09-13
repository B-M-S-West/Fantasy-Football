import csv
import os
import shutil

def directory_reset():
    if os.path.exists("csv"):
        shutil.rmtree("csv")
    os.mkdir("csv")

def write_csv(filename, headers, data):
    with open(f'csv/{filename}', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

def weekly_score(entry_id_to_name_map, current_gameweek, gameweek_ranks):
    headers = ['Manager'] + [f'GW{i}' for i in range(1, current_gameweek + 1)]
    data = [[entry_id_to_name_map[entry]] + ranks for entry, ranks in gameweek_ranks.items()]
    write_csv('weekly_score.csv', headers, data)

def total_score_progression(entry_id_to_name_map, current_gameweek, total_scores):
    headers = ['Manager'] + [f'GW{i}' for i in range(1, current_gameweek + 1)]
    data = [[entry_id_to_name_map[entry]] + scores for entry, scores in total_scores.items()]
    write_csv('totalScoreProgression.csv', headers, data)

def best_players_per_manager(best_players_per_manager):
    headers = ['Rank'] + list(best_players_per_manager.keys())
    max_players = max(len(players) for players in best_players_per_manager.values())
    data = []
    for i in range(max_players):
        row = [i + 1]
        for manager in best_players_per_manager:
            if i < len(best_players_per_manager[manager]):
                player = best_players_per_manager[manager][i]
                row.append(f"{player['elementName']} - {player['points']}")
            else:
                row.append('')
        data.append(row)
    write_csv('bestPlayersPerManager.csv', headers, data)

def best_clubs_per_manager(best_clubs_per_manager):
    headers = ['Rank'] + list(best_clubs_per_manager.keys())
    max_clubs = max(len(clubs) for clubs in best_clubs_per_manager.values())
    data = []
    for i in range(max_clubs):
        row = [i + 1]
        for manager in best_clubs_per_manager:
            if i < len(best_clubs_per_manager[manager]):
                club = best_clubs_per_manager[manager][i]
                row.append(f"{club['name']} - {club['points']}")
            else:
                row.append('')
        data.append(row)
    write_csv('bestClubsPerManager.csv', headers, data)

def best_players_overall(best_players_overall):
    headers = ['Rank', 'Name', 'Points', 'Appearances', 'Goals', 'Assists', 'Clean Sheets', 'Saves', 'Bonus']
    data = [[i+1] + [player[stat] for stat in ['elementName', 'points', 'appearances', 'goals', 'assists', 'clean_sheets', 'saves', 'bonus']] 
            for i, player in enumerate(best_players_overall)]
    write_csv('bestPlayersOverall.csv', headers, data)

def best_managers_by_position(league_entries, best_managers_by_position):
    headers = ['Rank'] + list(best_managers_by_position.keys())
    data = []
    for i in range(len(league_entries)):
        row = [i + 1]
        for position in best_managers_by_position:
            manager = best_managers_by_position[position][i]
            row.append(f"{manager['name']} - {manager['points']}")
        data.append(row)
    write_csv('bestManagersByPosition.csv', headers, data)

def best_managers_by_action(league_entries, best_managers_by_action):
    headers = ['Rank'] + list(best_managers_by_action.keys())
    data = []
    for i in range(len(league_entries)):
        row = [i + 1]
        for action in best_managers_by_action:
            manager = best_managers_by_action[action][i]
            row.append(f"{manager['name']} - {manager['points']}")
        data.append(row)
    write_csv('bestManagersByAction.csv', headers, data)

def most_transfers_by_manager(most_transfers_by_manager):
    headers = ['Name', 'TotalTransfers', 'SuccessfulWaivers', 'FreeTransfers', 'DeniedWaivers', 'BackupWaivers']
    data = [[manager['name'], manager['total_transfers'], manager['successful_waivers'], 
             manager['free_transfers'], manager['denied_waivers'], manager['backup_waivers']]
            for manager in most_transfers_by_manager]
    write_csv('mostTransfersByManager.csv', headers, data)

def most_transferred_players(most_transferred_players):
    headers = ['Name', 'TeamsPlayedFor', 'SuccessfulTransfers']
    data = [[player['name'], player['unique_transfers'], player['successful_transfers']]
            for player in most_transferred_players]
    write_csv('mostTransferredPlayers.csv', headers, data)