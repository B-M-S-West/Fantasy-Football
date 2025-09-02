import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import httpx
    import os
    from dotenv import load_dotenv
    import polars as pl
    import duckdb
    import plotly.express as px
    from typing import Dict, List
    return Dict, List, duckdb, httpx, load_dotenv, mo, os, pl


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Fantasy Draft Premier League Statistics
    This is a marimo python application for display data from a Fantasy Premier Draft league. All you need to input is the code for your draft league and then run the application for it to populate everything in all of the tables and the statistics diagrams. Contact me for any additional functionality required or things to put into a roadmap. This is just a fun personal project.
    """
    )
    return


@app.cell
def _():
    GAME_STATUS_URL = 'https://draft.premierleague.com/api/game'
    ELEMENT_INFO_URL = 'https://draft.premierleague.com/api/bootstrap-static'
    LEAGUE_DATA_URL = 'https://draft.premierleague.com/api/league/{}/details'
    ENTRY_PICKS_URL = 'https://draft.premierleague.com/api/entry/{}/event/{}'
    ELEMENT_STATS_URL = 'https://draft.premierleague.com/api/event/{}/live'
    TRANSFERS_URL = 'https://draft.premierleague.com/api/draft/league/{}/transactions'
    DRAFTS_URL = 'https://draft.premierleague.com/api/draft/{}/choices'
    MANAGER_HISTORY_URL = 'https://draft.premierleague.com/api/entry/{}/history'
    return LEAGUE_DATA_URL, MANAGER_HISTORY_URL


@app.cell
def _(load_dotenv, os):
    load_dotenv()
    league_id = os.getenv('LEAGUE_ID')
    entry_id = os.getenv('ENTRY_ID')
    return


@app.cell
def _(Dict, LEAGUE_DATA_URL, List, MANAGER_HISTORY_URL, httpx):
    def fetch_data(url: str) -> Dict:
        response = httpx.get(url)
        return response.json()

    def get_league_data(league_id: str) -> Dict:
        url = (LEAGUE_DATA_URL).format(league_id)
        return fetch_data(url)

    def get_manager_history(entry_id: int) -> List:
        url = (MANAGER_HISTORY_URL).format(entry_id)
        return fetch_data(url)["history"]
    return (get_league_data,)


@app.cell
def _(duckdb, get_league_data, league_id_input, pl):
    def process_league_data():
        league_data = get_league_data(league_id_input.value)
        league_entries = league_data['league_entries']
    
        # Convert to Polars DataFrame
        entries_df = pl.DataFrame(league_entries)
    
        # Create DuckDB table
        duckdb.sql("CREATE TABLE IF NOT EXISTS league_entries AS SELECT * FROM entries_df")
    
        return entries_df
    return


if __name__ == "__main__":
    app.run()
