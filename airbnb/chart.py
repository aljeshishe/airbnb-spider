import plotly.express as px

px.set_mapbox_access_token(
    "pk.eyJ1IjoiYWxqZXNoaXNoZSIsImEiOiJjbGJwaHJiajMwc3pxM3FxaDc4anltemN1In0.XZoRGDAvlJjbC21qfZTJcA")


def create_chart(df):
    fig = px.scatter_mapbox(df,
                            lat="listing_coordinate_latitude", lon="listing_coordinate_longitude",
                            color="price",
                            size="rating",
                            center=dict(lat=36.854598, lon=28.261513), zoom=5,
                            size_max=10,
                            # color_continuous_scale="sunset",
                            color_continuous_scale=["rgb(248, 160, 126)", "rgb(92, 83, 165)"],
                            custom_data=["listing_id"],
                            hover_data=["rating", "reviews", "price", "discount", "listing_roomTypeCategory"],
                            height=1000)
    fig.update_layout({"margin": {"l": 10, "r": 10, "t": 10, "b": 10}})
    # fig.update_traces(cluster=dict(enabled=True))
    return fig
