import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def create(df: pd.DataFrame) -> go.Figure:
    y, x = np.histogram(df.price, bins=120, range=(0, 2000))
    fig = px.bar(x=x[:-1], y=y, labels={"x": "Price", "y": "Count"})

    fig.update_layout(
        {
            # "template": template,
            "barmode": "overlay",
            "selectionrevision": True,
            "height": 150,
            "margin": {"l": 10, "r": 10, "t": 10, "b": 10},
            "xaxis": {
                "autorange": True,
                # "automargin": True,
                "title": {"text": "Price"}
            },
            "yaxis": {
                "autorange": True,
                # "automargin": True,
                "title": {"text": "Count"},
            },
            "selectdirection": "h",
            "hovermode": "closest",
            "dragmode": "select",
        }
    )
    # set ticks
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=25
        )
    )
    return fig
