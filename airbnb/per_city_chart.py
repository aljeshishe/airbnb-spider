import plotly.express as px


def create(df):
    fig = px.scatter_mapbox(df,
                            lat="listing_coordinate_latitude", lon="listing_coordinate_longitude",
                            size="count",
                            center=dict(lat=36.854598, lon=28.261513), zoom=5,
                            color_discrete_sequence=["rgb(92, 83, 165)"],
                            size_max=10,
                            # color_continuous_scale="sunset",
                            # color_continuous_scale=["rgb(248, 160, 126)", "rgb(92, 83, 165)"],
                            # custom_data=["listing_id"],
                            hover_data=["listing_city", "count"],
                            height=1000)
    return fig
