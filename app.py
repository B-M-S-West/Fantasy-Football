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
    return Dict, List, duckdb, httpx, load_dotenv, mo, os, pl, px


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
    return (league_id,)


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
    return get_league_data, get_manager_history


@app.cell
def _(duckdb, entries_df, get_league_data, league_id, pl):
    def process_league_data():
        league_data = get_league_data(league_id)
        league_entries = league_data['league_entries']
    
        # Convert to Polars DataFrame
        entries_df = pl.DataFrame(league_entries)
    
        # Create DuckDB table
        duckdb.sql("CREATE TABLE IF NOT EXISTS league_entries AS SELECT * FROM entries_df")
    
        return entries_df
    return (process_league_data,)


@app.cell
def _(duckdb, get_manager_history, history_df, pl):
    def process_historical_data(entries_df):
        all_history = []
    
        for entry_id in entries_df['entry_id']:
            history = get_manager_history(entry_id)
            for event in history:
                event['entry_id'] = entry_id
                all_history.append(event)
    
        history_df = pl.DataFrame(all_history)
    
        # Create DuckDB table
        duckdb.sql("CREATE TABLE IF NOT EXISTS manager_history AS SELECT * FROM history_df")
    
        return history_df
    return


@app.cell
def _(mo, pl, px):
    def create_leaderboard(history_df, entries_df):
        # Join history with entry information
        plot_data = history_df.join(
            entries_df.select(['entry_id', 'player_first_name', 'player_last_name']),
            on='entry_id'
        )
    
        # Create manager name column
        plot_data = plot_data.with_columns([
            pl.concat_str([
                pl.col('player_first_name'),
                pl.lit(' '),
                pl.col('player_last_name')
            ]).alias('manager_name')
        ])
    
        # Create line plot
        fig = px.line(
            plot_data.to_pandas(),
            x='event',
            y='total_points',
            color='manager_name',
            title='Fantasy League Points Progression'
        )
    
        return mo.md(f"## League Standings\n{fig}")
    return


@app.cell
def _(duckdb, mo):
    def player_points_leaderboard(entries_df):
        query = """
        SELECT 
            e.player_first_name || ' ' || e.player_last_name as manager,
            h.points,
            h.event as gameweek
        FROM manager_history h
        JOIN league_entries e ON h.entry_id = e.entry_id
        ORDER BY h.points DESC
        LIMIT 10
        """
    
        top_scores = duckdb.sql(query).df()
    
        return mo.md(f"""
        ## Top Gameweek Performances
        {top_scores.to_markdown()}
        """)
    return


@app.cell
def _(mo):
    def create_interactive_elements():
        gameweek_selector = mo.ui.slider(1, 38, label="Select Gameweek")
        return gameweek_selector
    return


@app.cell
def _(duckdb, mo):
    def gameweek_analysis(gameweek_selector):
        query = f"""
        SELECT 
            e.player_first_name || ' ' || e.player_last_name as manager,
            h.points
        FROM manager_history h
        JOIN league_entries e ON h.entry_id = e.entry_id
        WHERE h.event = {gameweek_selector.value}
        ORDER BY h.points DESC
        """
    
        gw_results = duckdb.sql(query).df()
    
        return mo.md(f"""
        ## Gameweek {gameweek_selector.value} Results
        {gw_results.to_markdown()}
        """)
    return


@app.cell
def _(process_league_data):
    process_league_data()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
