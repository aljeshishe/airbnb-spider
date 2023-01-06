import click

from airbnb import data
from pathlib import Path


@click.command()
@click.argument("result_path")
def convert(result_path: str):
    project_path = Path(__file__).parent.parent
    input_file = project_path / f"results/{result_path}"
    output_file = project_path / f"results/{result_path}.pkl.zip"
    print(f"Converting {input_file} to {output_file}")
    df = data.read_pickle_dir(input_file)
    df1 = data.delete_duplicates(df)
    df1.to_pickle(output_file)


if __name__ == "__main__":
    convert()
