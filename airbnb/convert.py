import click

from airbnb import data
from pathlib import Path
import rootpath
import pandas_utils as pu

pu.install()

@click.command()
@click.argument("result_path")
def convert(result_path: str):
    project_path = Path(rootpath.detect(__file__))

    input_file = project_path / f"results/{result_path}"
    output_file = project_path / f"results/{result_path}.pkl.zip"

    print(f"Converting {input_file} to {output_file}")
    df = data.read_pickle_dir(input_file).drop_duplicates(subset="listing_id").to_pickle(output_file)


if __name__ == "__main__":
    convert()
