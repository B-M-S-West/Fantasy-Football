import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import httpx
    import os
    from dotenv import load_dotenv
    import polars as pl
    import duckdb
    import plotly.express as px
    from typing import Dict, List
    import networkx as nx
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    return (
        Dict,
        List,
        duckdb,
        go,
        httpx,
        load_dotenv,
        make_subplots,
        mo,
        os,
        pl,
        px,
    )


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
def _(load_dotenv, mo, os):
    # Load environment variables or create input widget
    load_dotenv()
    env_league_id = os.getenv('LEAGUE_ID')

    # Create league ID input widget
    league_id_input = mo.ui.text(
        label="League ID", 
        value=env_league_id if env_league_id else "",
        placeholder="Enter your Fantasy Draft League ID"
    )

    league_id_input
    return (league_id_input,)


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
    return fetch_data, get_league_data, get_manager_history


@app.cell
def _(league_id_input):
    type(league_id_input)
    return


@app.cell
def _(duckdb, get_league_data, league_id_input, pl):
    def process_league_data(league_id_input):
        league_data = get_league_data(league_id_input)
        league_entries = league_data['league_entries']

        # Convert to Polars DataFrame
        entries_df = pl.DataFrame(league_entries)

        # Create DuckDB table
        duckdb.sql("CREATE TABLE IF NOT EXISTS league_entries AS SELECT * FROM entries_df")

        return entries_df
    entries_df = process_league_data(league_id_input.value)
    return (entries_df,)


@app.cell
def _(duckdb, entries_df, get_manager_history, pl):
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
    history_df = process_historical_data(entries_df)
    return (history_df,)


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
    return (create_leaderboard,)


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
    return (player_points_leaderboard,)


@app.cell
def _(mo):
    # Create a gameweek selector
    gameweek_selector = mo.ui.slider(1, 38, label="Select Gameweek")
    return (gameweek_selector,)


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
    return (gameweek_analysis,)


@app.cell
def _(api_config, duckdb, elements_df, fetch_data, pl, transfers_df):
    def process_transfers(league_id_input):
        transfers = fetch_data(api_config['TRANSFERS_URL'].format(league_id_input.value))
        element_info = fetch_data(api_config['ELEMENT_INFO_URL'])['elements']

        # Convert to Polars DataFrame
        transfers_df = pl.DataFrame(transfers['transactions'])
        elements_df = pl.DataFrame(element_info)

        # Create DuckDB tables
        duckdb.sql("CREATE TABLE IF NOT EXISTS transfers AS SELECT * FROM transfers_df")
        duckdb.sql("CREATE TABLE IF NOT EXISTS elements AS SELECT * FROM elements_df")

        return transfers_df, elements_df
    return


@app.cell
def _(duckdb, elements, league_entries, mo, px, transfers):
    def transfer_analysis_dashboard(transfers_df, elements_df, entries_df):
        # Transfer success rate by manager
        transfer_stats = duckdb.sql("""
            SELECT 
                e.player_first_name || ' ' || e.player_last_name as manager,
                COUNT(*) as total_transfers,
                SUM(CASE WHEN t.result = 'a' THEN 1 ELSE 0 END) as successful_transfers,
                ROUND(SUM(CASE WHEN t.result = 'a' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate
            FROM transfers t
            JOIN league_entries e ON t.entry = e.entry_id
            GROUP BY manager
            ORDER BY total_transfers DESC
        """).df()

        # Most transferred players
        player_transfers = duckdb.sql("""
            SELECT 
                el.web_name as player_name,
                COUNT(*) as transfer_attempts,
                SUM(CASE WHEN t.result = 'a' THEN 1 ELSE 0 END) as successful_transfers
            FROM transfers t
            JOIN elements el ON t.element_in = el.id
            GROUP BY el.web_name
            ORDER BY transfer_attempts DESC
            LIMIT 10
        """).df()

        # Create visualizations
        fig1 = px.bar(
            transfer_stats.to_pandas(),
            x='manager',
            y=['successful_transfers', 'total_transfers'],
            title='Transfer Activity by Manager'
        )

        fig2 = px.bar(
            player_transfers.to_pandas(),
            x='player_name',
            y=['successful_transfers', 'transfer_attempts'],
            title='Most Transferred Players'
        )

        return mo.md(f"""
        ## Transfer Analysis
        ### Manager Transfer Activity
        {fig1}

        ### Most Sought-After Players
        {fig2}

        ### Transfer Success Rates
        {transfer_stats.to_markdown()}
        """)
    return (transfer_analysis_dashboard,)


@app.cell
def _(mo, pl):
    def head_to_head_analysis(history_df, entries_df):
        # Create manager selector dropdowns
        manager1 = mo.ui.dropdown(
            options=entries_df.select(
                pl.concat_str([pl.col('player_first_name'), pl.lit(' '), pl.col('player_last_name')])
            ).to_series().to_list(),
            label="Select Manager 1"
        )
        manager2 = mo.ui.dropdown(
            options=entries_df.select(
                pl.concat_str([pl.col('player_first_name'), pl.lit(' '), pl.col('player_last_name')])
            ).to_series().to_list(),
            label="Select Manager 2"
        )

        return manager1, manager2
    return


@app.cell
def _(duckdb, go, make_subplots, mo):
    def display_head_to_head(manager1, manager2, history_df, entries_df):
        if not (manager1.value and manager2.value):
            return mo.md("Please select both managers to compare")

        query = f"""
        WITH manager1_data AS (
            SELECT 
                h.event,
                h.points as m1_points,
                h.total_points as m1_total
            FROM manager_history h
            JOIN league_entries e 
                ON h.entry_id = e.entry_id
            WHERE e.player_first_name || ' ' || e.player_last_name = '{manager1.value}'
        ),
        manager2_data AS (
            SELECT 
                h.event,
                h.points as m2_points,
                h.total_points as m2_total
            FROM manager_history h
            JOIN league_entries e 
                ON h.entry_id = e.entry_id
            WHERE e.player_first_name || ' ' || e.player_last_name = '{manager2.value}'
        )
        SELECT 
            m1.event,
            m1.m1_points,
            m2.m2_points,
            m1.m1_total,
            m2.m2_total
        FROM manager1_data m1
        JOIN manager2_data m2 ON m1.event = m2.event
        ORDER BY m1.event
        """

        comparison_data = duckdb.sql(query).df()

        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Gameweek Points Comparison', 'Total Points Progression')
        )

        # Gameweek points comparison
        fig.add_trace(
            go.Bar(name=manager1.value, x=comparison_data['event'], y=comparison_data['m1_points']),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(name=manager2.value, x=comparison_data['event'], y=comparison_data['m2_points']),
            row=1, col=1
        )

        # Total points progression
        fig.add_trace(
            go.Scatter(name=f"{manager1.value} (Total)", x=comparison_data['event'], y=comparison_data['m1_total']),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(name=f"{manager2.value} (Total)", x=comparison_data['event'], y=comparison_data['m2_total']),
            row=2, col=1
        )

        return mo.md(f"""
        ## Head-to-Head Comparison: {manager1.value} vs {manager2.value}
        {fig}
        """)
    return (display_head_to_head,)


@app.cell
def _(mo):
    def player_performance_dashboard():
        # Create player search input
        player_search = mo.ui.text(label="Search for a player")
        position_filter = mo.ui.dropdown(
            options=['All', 'Goalkeeper', 'Defender', 'Midfielder', 'Forward'],
            label="Filter by position"
        )

        return player_search, position_filter
    return


@app.cell
def _(duckdb, mo, px):
    def display_player_performance(player_search, position_filter):
        position_map = {
            'Goalkeeper': 1,
            'Defender': 2,
            'Midfielder': 3,
            'Forward': 4
        }

        position_clause = ""
        if position_filter.value != 'All':
            position_clause = f"AND element_type = {position_map[position_filter.value]}"

        search_clause = ""
        if player_search.value:
            search_clause = f"AND web_name ILIKE '%{player_search.value}%'"

        query = f"""
        SELECT 
            web_name,
            CASE element_type 
                WHEN 1 THEN 'Goalkeeper'
                WHEN 2 THEN 'Defender'
                WHEN 3 THEN 'Midfielder'
                WHEN 4 THEN 'Forward'
            END as position,
            team,
            total_points,
            goals_scored,
            assists,
            clean_sheets,
            minutes,
            points_per_game::FLOAT as ppg
        FROM elements
        WHERE 1=1 {position_clause} {search_clause}
        ORDER BY total_points DESC
        LIMIT 20
        """

        player_stats = duckdb.sql(query).df()

        fig = px.scatter(
            player_stats.to_pandas(),
            x='minutes',
            y='total_points',
            color='position',
            size='ppg',
            hover_data=['web_name', 'goals_scored', 'assists'],
            title='Player Performance Overview'
        )

        return mo.md(f"""
        ## Player Performance Analysis
        {fig}

        ### Top Performers
        {player_stats.to_markdown()}
        """)
    return (display_player_performance,)


@app.cell
def _(mo, pl):
    def team_composition_analysis(entries_df):
        # Create team selector
        team_selector = mo.ui.dropdown(
            options=entries_df.select(
                pl.concat_str([pl.col('player_first_name'), pl.lit(' '), pl.col('player_last_name')])
            ).to_series().to_list(),
            label="Select Team to Analyze"
        )
        gameweek_selector = mo.ui.slider(1, 38, label="Select Gameweek")
    return


@app.cell
def _(api_config, duckdb, fetch_data, mo, pl, px):
    def display_team_composition(team_selector, gameweek_selector, entries_df):
        if not team_selector.value:
            return mo.md("Please select a team to analyze")

        # Get entry_id for selected team
        entry_id = entries_df.filter(
            pl.concat_str([pl.col('player_first_name'), pl.lit(' '), pl.col('player_last_name')]) == team_selector.value
        ).select('entry_id').item()

        # Get team picks for selected gameweek
        picks = fetch_data(api_config['ENTRY_PICKS_URL'].format(entry_id, gameweek_selector.value))
        picks_df = pl.DataFrame(picks['picks'])

        # Join with element info
        query = """
        SELECT 
            e.web_name,
            e.team,
            CASE e.element_type 
                WHEN 1 THEN 'Goalkeeper'
                WHEN 2 THEN 'Defender'
                WHEN 3 THEN 'Midfielder'
                WHEN 4 THEN 'Forward'
            END as position,
            p.position as pick_position,
            e.total_points,
            e.points_per_game::FLOAT as ppg,
            CASE WHEN p.position <= 11 THEN 'Starting' ELSE 'Bench' END as status
        FROM picks p
        JOIN elements e ON p.element = e.id
        ORDER BY p.position
        """

        team_composition = duckdb.sql(query).df()

        # Create formation visualization
        fig = px.scatter(
            team_composition.to_pandas(),
            x='team',
            y='position',
            size='ppg',
            color='status',
            hover_data=['web_name', 'total_points'],
            title=f'Team Composition - GW{gameweek_selector.value}'
        )

        return mo.md(f"""
        ## Team Composition Analysis for {team_selector.value}

        ### Squad Overview
        {fig}

        ### Squad Details
        {team_composition.to_markdown()}
        """)
    return (display_team_composition,)


@app.cell
def _(mo):
    def main_dashboard():
        return mo.md(f"""
        # Fantasy Premier League Draft Analytics Dashboard

        ## Quick Navigation
        - [League Standings](#league-standings)
        - [Transfer Analysis](#transfer-analysis)
        - [Head-to-Head Comparison](#head-to-head-comparison)
        - [Player Performance](#player-performance-analysis)
        - [Team Composition](#team-composition-analysis)

        Enter your league ID above to get started!
        """)
    return


@app.cell
def _(
    create_leaderboard,
    mo,
    player_points_leaderboard,
    transfer_analysis_dashboard,
):
    dashboard = mo.ui.tabs({
            "Leaderboard": create_leaderboard,
            "Top Performances": player_points_leaderboard,
            "Transfers": transfer_analysis_dashboard,
        })
    return


@app.cell
def _(gameweek_selector, league_id_input, mo):
    sidebar = mo.sidebar(
            [
                mo.md("### ⚙️ Settings"),
                league_id_input,
                gameweek_selector,
            ],
            footer=mo.md("Made with ❤️ and marimo"),
            width="280px"
        )
    return (sidebar,)


@app.cell
def _(
    create_leaderboard,
    display_head_to_head,
    display_player_performance,
    display_team_composition,
    elements_df,
    entries_df,
    gameweek_analysis,
    gameweek_selector,
    history_df,
    manager1,
    manager2,
    mo,
    player_points_leaderboard,
    player_search,
    position_filter,
    team_selector,
    transfer_analysis_dashboard,
    transfers_df,
):
    tabs = mo.ui.tabs({
            "📊 League Standings": create_leaderboard(history_df, entries_df),
            "🏆 Top Performances": player_points_leaderboard(entries_df),
            "⏳ Gameweek Results": gameweek_analysis(gameweek_selector),
            "🔄 Transfers": transfer_analysis_dashboard(transfers_df, elements_df, entries_df),
            "🤝 Head-to-Head": display_head_to_head(manager1, manager2, history_df, entries_df),
            "⚡ Player Performance": display_player_performance(player_search, position_filter),
            "📝 Team Composition": display_team_composition(team_selector, gameweek_selector, entries_df),
        })
    return (tabs,)


@app.cell
def _(mo, sidebar, tabs):
    layout = mo.vstack([sidebar, tabs])
    layout
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
