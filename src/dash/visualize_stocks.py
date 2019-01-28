"""

"""


## IMPORTED LIBRARIES

import dash as da
import dash.dependencies as dep
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Interface for environment variable input
import os

# Manipulate PostgreSQL/TimescaleDB data as Pandas dataframe
import pandas as pd

# Enable driver for PostgreSQL connection objects
import psycopg2

# Enable database interactions
import sqlalchemy as sqla

# Enable dedentation of multi-line strings
import textwrap as tw


## GLOBAL PARAMETERS
PSQL_USER = os.environ["HENG_TIMESCALE_DB_USER"]
PSQL_PASS = os.environ["HENG_TIMESCALE_DB_PASS"]
PSQL_HOST = os.environ["HENG_TIMESCALE_DB_HOST"]
PSQL_PORT = os.environ["HENG_TIMESCALE_DB_PORT"]
PSQL_NAME = os.environ["HENG_TIMESCALE_DB_NAME"]

# Create PostgreSQL/TimescaleDB session
psql = sqla \
       .create_engine(f"postgresql+psycopg2://{PSQL_USER}:{PSQL_PASS}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_NAME}") \
       .connect()

# Sets Dash application parameters
app = da.Dash("Charge_Tracker",
              external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])
server = app.server
app.layout = html.Div([
    html.Div([
        dcc.Markdown(tw.dedent("""
                **Movement volume change**
                Reports the movement volume change of stock in 15 minute window.
                Updates every minute.
            """)),
        dcc.Graph(
            id="sentiment_volume_change",
            figure="figure"),
        dcc.Interval(
            id="real_time_updates",
            interval=60000,
            n_intervals=0)],
        style={
            "width": "100%",
            "height": "auto",
            "display": "scatter",
            "padding-bottom": "75px"}
    ),
],
    style={
        "width": "99%",
        "height": "auto", }
)

## FUNCTION DEFINITIONS

def query_postgres_stocks(symbol, start_datetime, end_datetime):
    """
    Queries PostgreSQL/TimescaleDB database according to input query parameters.
    """
    # Create and execute SQL query
    query = """
            SELECT
                symbol,
                companyName,
                latestTime,
                movementVolume
            FROM
                stock_market_data
            WHERE
                symbol = '{}' AND
                latestTime BETWEEN '{}' AND '{}'
            ORDER BY
                latestTime
                    ASC
            """ \
            .format(symbol, start_datetime, end_datetime)
    result = psql.execute(query)

    df_stocks = pd.DataFrame([i for i in result])
    df_stocks.columns = ["symbol", "companyName", "latestTime", "movementVolume"]

    return df_stocks

# Callback updates graph (OUTPUT) according to time interval (INPUT)
@app.callback(dep.Output("sentiment_volume_change", "figure"),
              [dep.Input("real_time_updates", "n_intervals")])
def update_graph(interval):
    """
    Queries table, analyzes data, and assembles results in Dash format.
    """
    # TODO: Replace hardcoded results with dcc callbacks
    df_stocks = query_postgres_stocks("BA", "2019-01-28 18:05:03-05", "2019-01-28 19:00:00-05")

    # Creates scatter data for real-time graph
    plot_stocks = go.Scatter(x = df_stocks["latestTime"],
                             y = df_stocks["movementVolume"],
                        )

    data = [plot_stocks]

    # Sets Dashboard figure layout
    layout = go.Layout(hovermode = "closest",
                       legend = {"orientation": "h"},
                       margin = {"l": 100, "b": 40, "t": 10, "r": 10},
                       xaxis = {"title": "Date",
                                "gridcolor": "rgb(255,255,255)",
                                "showgrid": True,
                                "showline": False,
                                "showticklabels": True,
                                "tickcolor": "rgb(127,127,127)",
                                "ticks": "outside",
                                "zeroline": False},
                       yaxis = {"title": "Movement volume",
                                "gridcolor": "rgb(255,255,255)",
                                "showgrid": True,
                                "showline": False,
                                "showticklabels": True,
                                "tickcolor": "rgb(127,127,127)",
                                "ticks": "outside",
                                "zeroline": False},)

    return go.Figure(data = data, layout = layout)


## MAIN MODULE
if __name__ == "__main__":
    app.run_server(debug = False,
                   host = "0.0.0.0",
                   port = 5000)
