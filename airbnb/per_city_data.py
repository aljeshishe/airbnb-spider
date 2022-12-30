import pandas as pd

def filter_price(df: pd.DataFrame, treshold: float) -> pd.DataFrame:
    return df[df["price"] < treshold]

def group_per_city(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("listing_city").\
        agg({"listing_id": "count",
             "listing_coordinate_latitude": "mean",
             "listing_coordinate_longitude": "mean"}
            ).rename(columns={"listing_id": "count"}).reset_index()

