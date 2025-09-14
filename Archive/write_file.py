import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import shutil
from openpyxl import Workbook
import csv

# Load environment variables
load_dotenv()

# The ID of your spreadsheet
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

# Path to your service account JSON file
SERVICE_ACCOUNT_FILE = 'fantasyfootball-draft.json'

# If modifying these scopes, make sure you have the correct permissions in your service account
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_sheets_service():
  creds = Credentials.from_service_account_file(
      SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  return build('sheets', 'v4', credentials=creds)

def write_to_sheet(service, sheet_name, headers, data):
  # Prepare the data
  values = [headers] + data

  body = {
      'values': values
  }

  # Check if the sheet exists, if not create it
  try:
      service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID, ranges=sheet_name).execute()
  except:
      request_body = {
          'requests': [{
              'addSheet': {
                  'properties': {
                      'title': sheet_name
                  }
              }
          }]
      }
      service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=request_body).execute()

  # Write to the sheet
  result = service.spreadsheets().values().update(
      spreadsheetId=SPREADSHEET_ID,
      range=f'{sheet_name}!A1',
      valueInputOption='USER_ENTERED',
      body=body
  ).execute()

  print(f'{result.get("updatedCells")} cells updated in {sheet_name}.')

def directory_reset():
    if os.path.exists("excel"):
        shutil.rmtree("excel")
    os.mkdir("excel")
    if os.path.exists("csv"):
        shutil.rmtree("csv")
    os.mkdir("csv")

def write_excel(filename, headers, data):
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    for row in data:
        ws.append(row)
    wb.save(f'excel/{filename}')
    print(f"Excel file saved: excel/{filename}")

def write_csv(filename, headers, data):
    with open(f'csv/{filename}', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)


def weekly_score(entry_id_to_name_to_team_map, current_gameweek, gameweek_scores):
  headers = ['Manager', 'Team'] + [f'GW{i}' for i in range(1, current_gameweek + 1)]
  data = [[manager, team] + scores for entry_id, (manager, team) in entry_id_to_name_to_team_map.items() if entry_id in gameweek_scores for scores in [gameweek_scores[entry_id]]]
  write_to_sheet(get_google_sheets_service(), 'Weekly Score', headers, data)

  headers = ['Manager', 'Team', 'Gameweek', 'Points']
  data = [[manager, team, i + 1, score] for entry_id, (manager, team) in entry_id_to_name_to_team_map.items() if entry_id in gameweek_scores for i, score in enumerate(gameweek_scores[entry_id])]
  write_to_sheet(get_google_sheets_service(), 'Weekly Score (Detailed)', headers, data)
  write_excel('weekly_score.xlsx', headers, data)
  write_csv('weekly_score.csv', headers, data)

def total_score_progression(entry_id_to_name_to_team_map, current_gameweek, total_scores):
  headers = ['Manager', 'Team'] + [f'GW{i}' for i in range(1, current_gameweek + 1)]
  data = [[manager, team] + scores for entry_id, (manager, team) in entry_id_to_name_to_team_map.items() if entry_id in total_scores for scores in [total_scores[entry_id]]]
  write_to_sheet(get_google_sheets_service(), 'Total Score Progression', headers, data)
  write_excel('totalScoreProgression.xlsx', headers, data)
  write_csv('totalScoreProgression.csv', headers, data)

  headers = ['Manager', 'Team', 'Gameweek', 'Total Points']
  data = [[manager, team, i + 1, score] for entry_id, (manager, team) in entry_id_to_name_to_team_map.items() if entry_id in total_scores for i, score in enumerate(total_scores[entry_id])]
  write_to_sheet(get_google_sheets_service(), 'Total Score Progression (Detailed)', headers, data)

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
  write_to_sheet(get_google_sheets_service(), 'Best Players Per Manager', headers, data)
  write_excel('bestPlayersPerManager.xlsx', headers, data)
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
  write_to_sheet(get_google_sheets_service(), 'Best Clubs Per Manager', headers, data)
  write_excel('bestClubsPerManager.xlsx', headers, data)
  write_csv('bestClubsPerManager.csv', headers, data)

def best_players_overall(best_players_overall):
  headers = ['Rank', 'Name', 'Points', 'Appearances', 'Goals', 'Assists', 'Clean Sheets', 'Saves', 'Bonus']
  data = [[i+1] + [player[stat] for stat in ['elementName', 'points', 'appearances', 'goals', 'assists', 'clean_sheets', 'saves', 'bonus']] 
          for i, player in enumerate(best_players_overall)]
  write_to_sheet(get_google_sheets_service(), 'Best Players Overall', headers, data)
  write_excel('bestPlayersOverall.xlsx', headers, data)
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
  write_to_sheet(get_google_sheets_service(), 'Best Managers By Position', headers, data)
  write_excel('bestManagersByPosition.xlsx', headers, data)
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
  write_to_sheet(get_google_sheets_service(), 'Best Managers By Action', headers, data)
  write_excel('bestManagersByAction.xlsx', headers, data)
  write_csv('bestManagersByAction.csv', headers, data)

def most_transfers_by_manager(most_transfers_by_manager):
  headers = ['Name', 'TotalTransfers', 'SuccessfulWaivers', 'FreeTransfers', 'DeniedWaivers', 'BackupWaivers']
  data = [[manager['name'], manager['total_transfers'], manager['successful_waivers'], 
           manager['free_transfers'], manager['denied_waivers'], manager['backup_waivers']]
          for manager in most_transfers_by_manager]
  write_to_sheet(get_google_sheets_service(), 'Most Transfers By Manager', headers, data)
  write_excel('mostTransfersByManager.xlsx', headers, data)
  write_csv('mostTransfersByManager.csv', headers, data)

def most_transferred_players(most_transferred_players):
  headers = ['Name', 'TeamsPlayedFor', 'SuccessfulTransfers']
  data = [[player['name'], player['unique_transfers'], player['successful_transfers']]
          for player in most_transferred_players]
  write_to_sheet(get_google_sheets_service(), 'Most Transferred Players', headers, data)
  write_excel('mostTransferredPlayers.xlsx', headers, data)
  write_csv('mostTransferredPlayers.csv', headers, data)

