import webbrowser

import click
import dash
from dash import dcc, html, no_update
from dash.dependencies import Input, Output

from airbnb import data, per_city_data, prices_graph, listings_graph, per_city_graph
from airbnb_spider.lib import utils
from web.utils import to_path

MAX_LISTINGS_DISPLAYED = 50000
CHECK_IN_DATE = "2023-02-01"
CHECK_OUT_DATE = "2023-03-01"


@click.command
@click.argument("result_path")
def main(result_path: str):
    path = to_path(result_path)
    df = data.load(path)
    df = df.sort_values(by="price")
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
        dcc.Graph(id="price-histogram", figure=prices_graph.create(df), config={"displayModeBar": False}),
        dcc.Dropdown(categories, ["entire_home"], multi=True, id="category-dropdown"),
        dcc.Markdown(id="filter-output"),
        dcc.Tabs([
            dcc.Tab(label="Listings", children=[dcc.Graph(id="listings-graph", clear_on_unhover=True)]),
            dcc.Tab(label="Per city", children=[dcc.Graph(id="per-city-graph")]),
        ]),
        dcc.Tooltip(id="listings-graph-tooltip"),
        html.Div(id="dummy-div", style={"display": "none"}),
    ])

    @app.callback(
        Output("listings-graph-tooltip", "show"),
        Output("listings-graph-tooltip", "bbox"),
        Output("listings-graph-tooltip", "children"),
        Input("listings-graph", "hoverData"),
    )
    def display_hover(hoverData):
        if hoverData is None:
            return False, no_update, no_update

        # demo only shows the first point, but other points may also be available
        pt = hoverData["points"][0]
        bbox = pt["bbox"]

        listing_id = hoverData["points"][0]["customdata"][0]
        df_row = df[df["listing_id"] == listing_id]
        price = df_row["price"].values[0]
        discount = df_row["discount"].values[0]
        rating = df_row["rating"].values[0]
        reviews = df_row["reviews"].values[0]
        markdown = f"""**{price}$** discount:**{discount:.0f}%** rating:**{rating:.1f}** reviews:**{reviews}**"""
        children = [dcc.Markdown(markdown)]
        return True, bbox, children

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
        show_df = filtered_df[:MAX_LISTINGS_DISPLAYED]
        hidden_str = ""
        if hidden_count := len(filtered_df) - len(show_df):
            hidden_str = f"Hidden: **{hidden_count}**"
        listings_fig = listings_graph.create(show_df)

        per_city_fig = per_city_graph.create(per_city_data.group_per_city(df=filtered_df))
        return listings_fig, \
               per_city_fig, \
               f"Total: **{len(df)}** Filtered: **{len(filtered_df)}** {hidden_str} Price: {low:.1f} - {high:.1f}"

    # handles on_click and opnes browser
    @app.callback(
        Output("dummy-div", "children"),
        Input("listings-graph", "clickData"))
    def graph_click_opens_url(clickData):
        if clickData:
            listing_id = clickData["points"][0]["customdata"][0]
            df_row = df[df["listing_id"] == listing_id]
            check_in_date = df_row["check_in_date"].values[0] if "check_in_date" in df.columns else CHECK_IN_DATE
            check_out_date = df_row["check_out_date"].values[0] if "check_out_date" in df.columns else CHECK_OUT_DATE
            url = f"https://www.airbnb.ru/rooms/{listing_id}?adults=1&check_in={check_in_date}&check_out={check_out_date}"
            webbrowser.open(url, new=2, autoraise=False)
        return dash.no_update

    app.run_server(debug=True, port=utils.get_free_port(8080),
                   use_reloader=False, exclude_patterns=[r"*.pkl.zip"]
                   )


if __name__ == "__main__":
    main()
