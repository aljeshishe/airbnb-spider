import numpy as np
import plotly.express as px

px.set_mapbox_access_token(
    "pk.eyJ1IjoiYWxqZXNoaXNoZSIsImEiOiJjbGJwaHJiajMwc3pxM3FxaDc4anltemN1In0.XZoRGDAvlJjbC21qfZTJcA")


def create(df):
    mean_lat = df["listing_coordinate_latitude"].mean()
    mean_lng = df["listing_coordinate_longitude"].mean()

    def normalize(series, min, max):
        scale = (max - min) / (series.max() - series.min())
        return scale * series + min - series.min(axis=0) * scale

    fig = px.scatter_mapbox(df,
                            lat="listing_coordinate_latitude", lon="listing_coordinate_longitude",
                            color="price",
                            size=normalize(np.clip(df["rating"], 4.0, 5.0), min=2, max=5),
                            center=dict(lat=mean_lat, lon=mean_lng),
                            zoom=5,
                            size_max=15,
                            # color_continuous_scale="sunset",
                            color_continuous_scale=["rgb(248, 160, 126)", "rgb(92, 83, 165)"],
                            # range_color=[0, 50],
                            custom_data=["listing_id"],
                            # hover_data=[],
                            height=1000,)

    fig.update_traces(hoverinfo="none", hovertemplate=None)
    fig.update_layout({"margin": {"l": 10, "r": 10, "t": 10, "b": 10}}, uirevision="Don't change")
    # fig.update_traces(cluster=dict(enabled=True))
    return fig
