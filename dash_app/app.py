import webbrowser

import dash
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output

from airbnb import data, chart, prices_chart

# data
df = data.load("../results/2022-12-21_02-59-19")
price_min = df["price"].min()
price_max = df["price"].max()

categories = df["listing_roomTypeCategory"].dropna().unique()



app = dash.Dash(__name__,
                external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
                compress=True)
app.layout = html.Div([
    html.H3("Airbnb listings"),
    dcc.Graph(id="price-histogram", figure=prices_chart.create(df), config={"displayModeBar": False}),
    dcc.Dropdown(categories, ["entire_home"], multi=True, id="category-dropdown"),
    html.Div(id="filter-output"),
    html.Div([dcc.Graph(id="graph")]),
    html.Div(id="dummy-div", style={"display": "none"}),
])


@app.callback(
    Output("graph", "figure"),
    Output("filter-output", "children"),
    Input("category-dropdown", "value"),
    Input("price-histogram", "selectedData"),
)
def price_category_changes_graph(category, price_selected_data):
    low, high = price_selected_data["range"]["x"] if price_selected_data else (price_min, price_max)
    filtered_df = df[
        (low <= df["price"]) &
        (df["price"] < high) &
        (df["listing_roomTypeCategory"].isin(category))
        ]
    fig = chart.create_chart(filtered_df)
    return fig, f"Showing {len(filtered_df)} from {len(df)} Price: {low:.1f} - {high:.1f}"


# handles on_click and opnes browser
@app.callback(
    Output("dummy-div", "children"),
    Input("graph", "clickData"))
def graph_click_opens_url(clickData):
    if clickData:
        id = clickData["points"][0]["customdata"][0]
        url = f"https://www.airbnb.ru/rooms/{id}?adults=1&check_in=2023-02-01&check_out=2023-02-07"
        webbrowser.open(url, autoraise=False)
    return dash.no_update


# check port is free
def check_port(port):
    import socket
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    try:
        s.bind(("", port))
        s.close()
        return True
    except socket.error:
        return False


def get_free_port(port):
    for p in range(port, 65535):
        if check_port(p):
            return p


app.run_server(debug=True, use_reloader=True, port=get_free_port(8080))
