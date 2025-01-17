"""Script for downloading new dataset."""

import click
import pandas as pd

DATASET_URL = "https://raw.githubusercontent.com/Mad0squirrel/MLOps-pet-project/master/research/data.csv"

@click.command()
@click.argument('output_dataset_file', type = click.Path(writable=True))
def cli(output_dataset_file: str) -> None:
     """Download data from DATASET_URL.

     Parameters
     ----------
      output_dataset_file : str
    
     Returns
     -------
     nothing

     """
     df = pd.read_csv(DATASET_URL, delimiter=';', on_bad_lines='skip')
     df.to_csv(output_dataset_file, index=False)
     
if __name__ == "__main__":
    cli()