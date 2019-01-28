"""

"""


# IMPORTED LIBRARIES
from dynamodb_json import json_util as dbjson

import boto3 as boto3
import dash as da
import dash.dependencies as dep
import dash_core_components as dcc

import dash_html_components as html
import datetime as dt
import os
import pandas as pd
import plotly.graph_objs as go
import textwrap as tw


# GLOBAL PARAMETERS
ACCESS_KEY = os.environ["HENG_AWS_ACCESS_KEY_ID"]
SECRET_KEY = os.environ["HENG_AWS_SECRET_ACCESS_KEY"]

# Create AWS DynamoDB session
dynamodb = boto3.Session(aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY,
                         region_name = "us-east-1") \
           .client("dynamodb")

# Sets Dash application parameters
app = da.Dash("Charge_Tracker",
              external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"])
server = app.server
app.layout = html.Div([
    html.Div([
        dcc.Markdown(tw.dedent("""
                **Sentiment volume change**
                Calculates number of tweets in current 15 minute window relative to previous 15 minute window.
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
def query_dynamodb_stocks(symbol, end_datetime, window_minutes):
    """
    Queries Cassandra database according to input CQL statement.
    """
    # Calculate start datetime
    start_datetime = end_datetime - dt.timedelta(minutes=window_minutes)

    # Convert start and end datetimes to formatted string representation
    start_datetime = dt.datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
    end_datetime = dt.datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S")

    # Collect query result
    result = dynamodb.query(TableName = "StockTradesProcessor",
                            Select = "SPECIFIC_ATTRIBUTES",
                            ProjectionExpression = "symbol, latestTime, companyName, movementVolume",
                            ExpressionAttributeValues = {":v1": {"S": symbol},
                                                         ":v2": {"S": start_datetime},
                                                         ":v3": {"S": end_datetime},},
                            KeyConditionExpression = "symbol = :v1 AND latestTime BETWEEN :v2 AND :v3",)

    # Extract query results
    if "Items" in result:
        df_stocks = pd.DataFrame(dbjson.loads(result["Items"]))
    else:
        df_stocks = pd.DataFrame(dbjson.loads(result["Item"]))

    # Convert datetime strings to datetime object representation
    df_stocks["latestTime"] = pd.to_datetime(df_stocks["latestTime"],
                                             format = "%Y-%m-%d %H:%M:%S")

    return df_stocks

# Callback updates graph (OUTPUT) according to time interval (INPUT)
@app.callback(dep.Output("sentiment_volume_change", "figure"),
              [dep.Input("real_time_updates", "n_intervals")])
def update_graph(interval):
    """
    Queries table, analyzes data, and assembles results in Dash format.
    """
    # TODO: Replace hardcoded results with dcc callbacks
    df_stocks = query_dynamodb_stocks("AAPL", dt.datetime(2019, 1, 3, 15, 5, 44), 15)

    # Creates scatter data for real-time graph
    plot_stocks = go.Scatter(x = df_stocks["latestTime"],
                             y = df_stocks["movementVolume"],
                             #hoverinfo = "text",
                             #legendgroup = "Group {}".format(c),
                             #line = {"color": colors[c][0]},
                             #mode = "lines+markers",
                             #name = "Group {}".format(c),
                             #text = mouseover_text,
                        )

    data = [plot_stocks]

    # Sets layout
    layout = go.Layout(hovermode = "closest",
                       legend = {"orientation": "h"},
                       margin = {"l": 40, "b": 40, "t": 10, "r": 10},
                       #paper_bgcolor = "rgb(255,255,255)",
                       #plot_bgcolor = "rgb(229,229,229)",
                       xaxis = {"title": "Date",
                                "gridcolor": "rgb(255,255,255)",
                                "showgrid": True,
                                "showline": False,
                                "showticklabels": True,
                                "tickcolor": "rgb(127,127,127)",
                                "ticks": "outside",
                                "zeroline": False},
                       yaxis = {"title": "Calculated energy  (Wh)",
                                "gridcolor": "rgb(255,255,255)",
                                "showgrid": True,
                                "showline": False,
                                "showticklabels": True,
                                "tickcolor": "rgb(127,127,127)",
                                "ticks": "outside",
                                "zeroline": False},)

    return go.Figure(data = data, layout = layout)


# MAIN MODULE
if __name__ == "__main__":
    app.run_server(debug = False,
                   host = "0.0.0.0",
                   port = 5000)