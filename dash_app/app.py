import webbrowser
from pathlib import Path

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

from airbnb import data, chart, prices_chart, per_city_chart, per_city_data

# data
# df = data.load("/Users/alexeygrachev/Desktop/git/airbnb-spider/results/2022-12-23_01-32-34") #asia
# df = data.load("/Users/alexeygrachev/Desktop/git/airbnb-spider/results/2022-12-23_03-58-51") #europe
df = data.load(Path(__file__).parent / "../results/2022-12-21_02-59-19") # south turkey
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
    html.Div([dcc.Graph(id="listings-graph")]),
    html.Div([dcc.Graph(id="per-city-graph")]),
    html.Div(id="dummy-div", style={"display": "none"}),
])


@app.callback(
    Output("listings-graph", "figure"),
    Output("per-city-graph", "figure"),
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
    listings_fig = chart.create_chart(filtered_df)

    per_city_fig = per_city_chart.create(per_city_data.group_per_city(df=filtered_df))
    return listings_fig, per_city_fig, f"Showing {len(filtered_df)} from {len(df)} Price: {low:.1f} - {high:.1f}"


# handles on_click and opnes browser
@app.callback(
    Output("dummy-div", "children"),
    Input("listings-graph", "clickData"))
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

