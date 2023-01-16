import shutil

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

    input_path = project_path / f"results/{result_path}"
    output_path = project_path / f"results/{result_path}.pkl.zip"

    print(f"Converting {input_path} to {output_path}")
    data.read_pickle_dir(input_path).drop_duplicates(subset="listing_id").to_pickle(output_path)

    answer = ""
    while answer.lower() not in ["y", "n"]:
        answer = input("Do you want to delete the original files? [y/n] ")
    if answer.lower() == "n":
        return

    shutil.rmtree(input_path, ignore_errors=True)



if __name__ == "__main__":
    convert()
