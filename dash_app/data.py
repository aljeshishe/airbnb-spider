import time

import click
import dtale

from airbnb import data
from dash_app.utils import to_path


@click.command
@click.argument("result_path")
def main(result_path: str):
    path = to_path(result_path)
    df = data.load(path)
    dtale.show(df).open_browser()
    time.sleep(100000000)


if __name__ == "__main__":
    main()
