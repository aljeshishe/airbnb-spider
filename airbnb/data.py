from pathlib import Path
from typing import Union

import pandas as pd
from tqdm import tqdm


def read_pickle_dir(path: Union[str, Path]) -> pd.DataFrame:
    path = Path(path) if isinstance(path, str) else path
    assert path.is_dir(), f"Expected a directory, got {path}"
    df = pd.concat((pd.read_pickle(file) for file in tqdm(list(path.glob(pattern="*.*")))), axis=0, ignore_index=True, copy=False)
    return df


def delete_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    # find duplicbates in dataframe
    print(f"Bfore {len(df)}")
    dups = df.duplicated(subset=["listing_id"])
    print(f"Duplicates {len(df[dups])}")
    dedup_df = df[~dups]
    print(f"After {len(dedup_df)}")
    return dedup_df


def enrich_df(df: pd.DataFrame) -> pd.DataFrame:
    # if no price, get discountedPrice
    # "From $1,000" -> "1000"
    price = df["pricingQuote_structuredStayDisplayPrice_primaryLine_price"].\
        fillna(df["pricingQuote_structuredStayDisplayPrice_primaryLine_discountedPrice"]).\
        str.replace("[^\d]", "", regex=True).\
        astype(float)
    df["price"] = price

    # "From $1,000" -> "1000"
    original_price = df["pricingQuote_structuredStayDisplayPrice_primaryLine_originalPrice"].\
        str.replace("[^\d]", "", regex=True).\
        astype(float)
    df["discount"] = ((1 - price / original_price) * 100).round(decimals=1)
    df["discount"] = df["discount"].fillna(value=0)

    df["new_place"] = df["listing_avgRatingLocalized"] == "New"
    df["listing_avgRatingLocalized"].replace("New", float("nan"), inplace=True, regex=True)

    tmpdf = df["listing_avgRatingLocalized"].str.replace("[/(|/)]", "", regex=True).str.split(expand=True)
    df["rating"] = tmpdf[0].astype(float).fillna(0)
    df["reviews"] = tmpdf[1].astype(float).fillna(0)
    return df


def load(path: Union[str, Path]) -> pd.DataFrame:
    path = path if isinstance(path, Path) else Path(path)
    if path.is_dir():
        df = read_pickle_dir(path)
    else:
        df = pd.read_pickle(path)
    df = delete_duplicates(df)
    df = df.dropna(subset=["listing_id"])
    df = enrich_df(df)
    return df

