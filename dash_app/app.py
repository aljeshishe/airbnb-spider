import webbrowser
from pathlib import Path

import click
import dash
import rootpath
from dash import dcc, html
from dash.dependencies import Input, Output

from airbnb import data, listings_chart, prices_chart, per_city_chart, per_city_data
from airbnb_spider.lib import utils

ROOT_PATH = Path(rootpath.detect(__file__))


def to_path(result_path: str) -> Path:
    path = Path(result_path)
    if path.exists():
        return path

    path = ROOT_PATH / "results" / result_path
    return path

@click.command
@click.argument("result_path")
def main(result_path:str):
    # data
    # df = data.load("/Users/alexeygrachev/Desktop/git/airbnb-spider/results/2022-12-23_01-32-34") #asia
    # df = data.load("/Users/alexeygrachev/Desktop/git/airbnb-spider/results/2022-12-23_03-58-51") #europe
    path = to_path(result_path)
    df = data.load(path)
    price_min = df["price"].min()
    price_max = df["price"].max()

    categories = df["listing_roomTypeCategory"].dropna().unique()

    app = dash.Dash(__name__,
                    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
                    compress=True)
    app.layout = html.Div([
        dcc.Markdown(f"""
## Airbnb listing
from **{path.parts[-1]}**
"""),
        dcc.Graph(id="price-histogram", figure=prices_chart.create(df), config={"displayModeBar": False}),
        dcc.Dropdown(categories, ["entire_home"], multi=True, id="category-dropdown"),
        html.Div(id="filter-output"),
        dcc.Tabs([
            dcc.Tab(label='Listings', children=[dcc.Graph(id="listings-graph")]),
            dcc.Tab(label='Per city', children=[dcc.Graph(id="per-city-graph")]),
        ]),
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
        listings_fig = listings_chart.create(filtered_df)

        per_city_fig = per_city_chart.create(per_city_data.group_per_city(df=filtered_df))
        return listings_fig, per_city_fig, f"Showing {len(filtered_df)} from {len(df)} Price: {low:.1f} - {high:.1f}"

    # handles on_click and opnes browser
    @app.callback(
        Output("dummy-div", "children"),
        Input("listings-graph", "clickData"))
    def graph_click_opens_url(clickData):
        if clickData:
            id = clickData["points"][0]["customdata"][0]
            url = f"https://www.airbnb.ru/rooms/{id}?adults=1&check_in=2023-02-01&check_out=2023-03-01"
            webbrowser.open(url, autoraise=False)
        return dash.no_update


    app.run_server(debug=True, use_reloader=False, port=utils.get_free_port(8080), exclude_patterns=[r"*.pkl.zip"])


if __name__ == "__main__":
    main()
