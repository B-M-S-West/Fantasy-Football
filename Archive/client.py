import requests

GAME_STATUS_URL = 'https://draft.premierleague.com/api/game'
ELEMENT_INFO_URL = 'https://draft.premierleague.com/api/bootstrap-static'
LEAGUE_DATA_URL = 'https://draft.premierleague.com/api/league/{}/details'
ENTRY_PICKS_URL = 'https://draft.premierleague.com/api/entry/{}/event/{}'
ELEMENT_STATS_URL = 'https://draft.premierleague.com/api/event/{}/live'
TRANSFERS_URL = 'https://draft.premierleague.com/api/draft/league/{}/transactions'
DRAFTS_URL = 'https://draft.premierleague.com/api/draft/{}/choices'
MANAGER_HISTORY_URL = 'https://draft.premierleague.com/api/entry/{}/history'

def get_game_status():
    response = requests.get(GAME_STATUS_URL)
    return response.json()

def get_element_info():
    response = requests.get(ELEMENT_INFO_URL)
    return response.json()

def get_league_data(league_id):
    url = LEAGUE_DATA_URL.format(league_id)
    response = requests.get(url)
    return response.json()

def get_entry_picks(entry_id, gameweek):
    url = ENTRY_PICKS_URL.format(entry_id, gameweek)
    response = requests.get(url)
    return response.json()['picks']

def get_element_stats(gameweek):
    url = ELEMENT_STATS_URL.format(gameweek)
    response = requests.get(url)
    return response.json()['elements']

def get_transfers(league_id):
    url = TRANSFERS_URL.format(league_id)
    response = requests.get(url)
    return response.json()['transactions']

def get_drafts(league_id):
    url = DRAFTS_URL.format(league_id)
    response = requests.get(url)
    return response.json()['choices']

def get_manager_history(entry_id):
    url = MANAGER_HISTORY_URL.format(entry_id)
    response = requests.get(url)
    return response.json()["history"]