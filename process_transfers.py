import client
import write_file

def run(league_id):
    league_data = client.get_league_data(league_id)
    league_entries = league_data['league_entries']
    transfers = client.get_transfers(league_id)
    element_info = client.get_element_info()['elements']

    entry_id_to_name_map = {entry['entry_id']: entry['player_first_name'] for entry in league_entries}

    transfers_by_manager = {entry['entry_id']: {'name': entry_id_to_name_map[entry['entry_id']], 
                                                'total_transfers': 0, 'successful_waivers': 0,
                                                'denied_waivers': 0, 'backup_waivers': 0, 
                                                'free_transfers': 0} for entry in league_entries}

    most_transferred_elements = {}

    for transfer in transfers:
        transfers_by_manager[transfer['entry']]['total_transfers'] += 1
        if transfer['element_in'] not in most_transferred_elements:
            most_transferred_elements[transfer['element_in']] = {
                'name': next((e['web_name'] for e in element_info if e['id'] == transfer['element_in']), 'Unknown'),
                'successful_transfers': 0,
                'unsuccessful_transfers': 0,
                'teams_played': [],
                'unique_transfers': 0,
            }

        if transfer['result'] == 'a':
            transfers_by_manager[transfer['entry']]['successful_waivers'] += 1
            most_transferred_elements[transfer['element_in']]['successful_transfers'] += 1
            if transfer['entry'] not in most_transferred_elements[transfer['element_in']]['teams_played']:
                most_transferred_elements[transfer['element_in']]['teams_played'].append(transfer['entry'])
                most_transferred_elements[transfer['element_in']]['unique_transfers'] += 1
        elif transfer['result'] == 'di':
            transfers_by_manager[transfer['entry']]['denied_waivers'] += 1
            most_transferred_elements[transfer['element_in']]['unsuccessful_transfers'] += 1
        elif transfer['result'] == 'do':
            transfers_by_manager[transfer['entry']]['backup_waivers'] += 1

    most_transfers_by_manager = sorted(transfers_by_manager.values(), key=lambda x: x['total_transfers'], reverse=True)
    most_uniquely_transferred_players = sorted(most_transferred_elements.values(), key=lambda x: (x['unique_transfers'], x['successful_transfers']), reverse=True)

    write_file.most_transfers_by_manager(most_transfers_by_manager)
    write_file.most_transferred_players(most_uniquely_transferred_players)

    print("Files generated for process_transfers.")