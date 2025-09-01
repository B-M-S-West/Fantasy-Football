import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import httpx
    import os
    from dotenv import load_dotenv
    return load_dotenv, mo, os


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
    return


@app.cell
def _(load_dotenv, os):
    load_dotenv()
    league_id = os.getenv('LEAGUE_ID')
    entry_id = os.getenv('ENTRY_ID')
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
