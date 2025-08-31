import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


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
    return


if __name__ == "__main__":
    app.run()
