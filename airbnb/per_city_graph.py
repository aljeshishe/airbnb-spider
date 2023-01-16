import plotly.express as px


def create(df):
    mean_lat = df["listing_coordinate_latitude"].mean()
    mean_lng = df["listing_coordinate_longitude"].mean()

    fig = px.scatter_mapbox(df,
                            lat="listing_coordinate_latitude", lon="listing_coordinate_longitude",
                            size="count",
                            center=dict(lat=mean_lat, lon=mean_lng),
                            zoom=5,
                            color_discrete_sequence=["rgb(92, 83, 165)"],
                            size_max=20,
                            # color_continuous_scale="sunset",
                            # color_continuous_scale=["rgb(248, 160, 126)", "rgb(92, 83, 165)"],
                            # custom_data=["listing_id"],
                            hover_data=["listing_city", "count"],
                            height=1000)
    fig.update_layout({"margin": {"l": 10, "r": 10, "t": 10, "b": 10}}, uirevision="Don't change")
    return fig

