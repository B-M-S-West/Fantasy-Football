import client
import write_csv
import write_excel
import write_google

def run(league_id):
    game_status = client.get_game_status()
    current_gameweek = game_status['current_event']

    element_and_team_info = client.get_element_info()
    element_info = element_and_team_info['elements']
    element_types = element_and_team_info['element_types']
    team_info = element_and_team_info['teams']

    league_data = client.get_league_data(league_id)
    league_entries = league_data['league_entries']

    entry_id_to_name_map = {entry['entry_id']: entry['player_first_name'] for entry in league_entries}

    entry_totals_per_element = {entry['entry_id']: {} for entry in league_entries}
    entry_totals_per_team = {entry['entry_id']: {} for entry in league_entries}
    element_totals = {}
    position_totals_per_entry = {1: {}, 2: {}, 3: {}, 4: {}}
    action_totals_per_entry = {
        'minutes': {}, 'goals': {}, 'assists': {}, 'clean_sheets': {},
        'saves': {}, 'penalty_saves': {}, 'bonus': {}, 'goals_conceded': {},
        'own_goals': {}, 'penalty_misses': {}, 'yellow_cards': {}, 'red_cards': {}
    }

    print("Starting detailed data pulls for process_point_breakdowns - this will take some time...")

    for gameweek in range(1, current_gameweek + 1):
        element_stats = client.get_element_stats(gameweek)
        for entry in league_entries:
            entry_id = entry['entry_id']
            team_picks = client.get_entry_picks(entry_id, gameweek)
            for element in team_picks[:11]:  # Only consider starting 11
                element_id = element['element']
                element_data = next(e for e in element_info if e['id'] == element_id)
                stats = element_stats[str(element_id)]['stats']

                # Update entry_totals_per_element
                if element_id not in entry_totals_per_element[entry_id]:
                    entry_totals_per_element[entry_id][element_id] = {
                        'id': element_id,
                        'elementName': element_data['web_name'],
                        'team': element_data['team'],
                        'position': element_data['element_type'],
                        'points': stats['total_points'],
                        'appearances': 1 if stats['minutes'] > 0 else 0,
                        'goals': stats['goals_scored'],
                        'assists': stats['assists'],
                        'clean_sheets': stats['clean_sheets'],
                        'saves': stats['saves'],
                        'bonus': stats['bonus'],
                    }
                else:
                    entry_totals_per_element[entry_id][element_id]['points'] += stats['total_points']
                    entry_totals_per_element[entry_id][element_id]['appearances'] += 1 if stats['minutes'] > 0 else 0
                    entry_totals_per_element[entry_id][element_id]['goals'] += stats['goals_scored']
                    entry_totals_per_element[entry_id][element_id]['assists'] += stats['assists']
                    entry_totals_per_element[entry_id][element_id]['clean_sheets'] += stats['clean_sheets']
                    entry_totals_per_element[entry_id][element_id]['saves'] += stats['saves']
                    entry_totals_per_element[entry_id][element_id]['bonus'] += stats['bonus']

                # Update entry_totals_per_team
                team_id = element_data['team']
                if team_id not in entry_totals_per_team[entry_id]:
                    entry_totals_per_team[entry_id][team_id] = {
                        'name': next(t['name'] for t in team_info if t['id'] == team_id),
                        'points': stats['total_points'],
                    }
                else:
                    entry_totals_per_team[entry_id][team_id]['points'] += stats['total_points']

                # Update element_totals
                if element_id not in element_totals:
                    element_totals[element_id] = {
                        'id': element_id,
                        'elementName': element_data['web_name'],
                        'team': element_data['team'],
                        'position': element_data['element_type'],
                        'points': stats['total_points'],
                        'appearances': 1 if stats['minutes'] > 0 else 0,
                        'goals': stats['goals_scored'],
                        'assists': stats['assists'],
                        'clean_sheets': stats['clean_sheets'],
                        'saves': stats['saves'],
                        'bonus': stats['bonus'],
                    }
                else:
                    element_totals[element_id]['points'] += stats['total_points']
                    element_totals[element_id]['appearances'] += 1 if stats['minutes'] > 0 else 0
                    element_totals[element_id]['goals'] += stats['goals_scored']
                    element_totals[element_id]['assists'] += stats['assists']
                    element_totals[element_id]['clean_sheets'] += stats['clean_sheets']
                    element_totals[element_id]['saves'] += stats['saves']
                    element_totals[element_id]['bonus'] += stats['bonus']

                # Update position_totals_per_entry
                position_id = element_data['element_type']
                if entry_id not in position_totals_per_entry[position_id]:
                    position_totals_per_entry[position_id][entry_id] = stats['total_points']
                else:
                    position_totals_per_entry[position_id][entry_id] += stats['total_points']

                # Update action_totals_per_entry
                for action, action_stats in action_totals_per_entry.items():
                    if entry_id not in action_stats:
                        action_stats[entry_id] = 0
                    
                    if action == 'minutes':
                        action_stats[entry_id] += 2 if stats['minutes'] > 60 else (1 if stats['minutes'] > 0 else 0)
                    elif action == 'goals':
                        action_stats[entry_id] += stats['goals_scored'] * (8 - position_id)
                    elif action == 'assists':
                        action_stats[entry_id] += stats['assists'] * 3
                    elif action == 'clean_sheets':
                        action_stats[entry_id] += stats['clean_sheets'] * (4 if position_id < 3 else (1 if position_id == 3 else 0))
                    elif action == 'saves':
                        action_stats[entry_id] += stats['saves'] // 3
                    elif action == 'penalty_saves':
                        action_stats[entry_id] += stats['penalties_saved'] * 5
                    elif action == 'bonus':
                        action_stats[entry_id] += stats['bonus']
                    elif action == 'goals_conceded':
                        action_stats[entry_id] += -1 * (stats['goals_conceded'] // 2) if position_id < 3 else 0
                    elif action == 'own_goals':
                        action_stats[entry_id] += stats['own_goals'] * -2
                    elif action == 'penalty_misses':
                        action_stats[entry_id] += stats['penalties_missed'] * -2
                    elif action == 'yellow_cards':
                        action_stats[entry_id] += stats['yellow_cards'] * -1
                    elif action == 'red_cards':
                        action_stats[entry_id] += stats['red_cards'] * -3

        print(f"Pulled and processed data for gameweek {gameweek}")

    best_players_per_manager = {
        entry_id_to_name_map[entry_id]: sorted(players.values(), key=lambda x: (x['points'], x['appearances']), reverse=True)
        for entry_id, players in entry_totals_per_element.items()
    }

    best_clubs_per_manager = {
        entry_id_to_name_map[entry_id]: sorted(clubs.values(), key=lambda x: x['points'], reverse=True)
        for entry_id, clubs in entry_totals_per_team.items()
    }

    best_players_overall = sorted(element_totals.values(), key=lambda x: (x['points'], x['appearances']), reverse=True)

    best_managers_by_position = {
        element_types[position_id - 1]['singular_name']: sorted(
            [{'name': entry_id_to_name_map[entry_id], 'points': points} for entry_id, points in managers.items()],
            key=lambda x: x['points'], reverse=True
        )
        for position_id, managers in position_totals_per_entry.items()
    }

    best_managers_by_action = {
        action: sorted(
            [{'name': entry_id_to_name_map[entry_id], 'points': points} for entry_id, points in managers.items()],
            key=lambda x: x['points'], reverse=True
        )
        for action, managers in action_totals_per_entry.items()
    }

    write_csv.best_players_per_manager(best_players_per_manager)
    write_excel.best_players_per_manager(best_players_per_manager)
    write_google.best_players_per_manager(best_players_per_manager)

    write_csv.best_clubs_per_manager(best_clubs_per_manager)
    write_excel.best_clubs_per_manager(best_clubs_per_manager)
    write_google.best_clubs_per_manager(best_clubs_per_manager)

    write_csv.best_players_overall(best_players_overall)
    write_excel.best_players_overall(best_players_overall)
    write_google.best_players_overall(best_players_overall)

    write_csv.best_managers_by_position(league_entries, best_managers_by_position)
    write_excel.best_managers_by_position(league_entries, best_managers_by_position)
    write_google.best_managers_by_position(league_entries, best_managers_by_position)
    
    write_csv.best_managers_by_action(league_entries, best_managers_by_action)
    write_excel.best_managers_by_action(league_entries, best_managers_by_action)
    write_google.best_managers_by_action(league_entries, best_managers_by_action)

    print("CSVs generated for process_point_breakdowns.")
