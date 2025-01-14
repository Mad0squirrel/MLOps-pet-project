"""Script for downloading features with overpass api."""

import json

import click
import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
AREA_BOUND = (55.41343, 37.29172, 56.04673, 38.01132)
ITEMS_KEY = 'elements'

def get_search_data(amenities: list[str], bound: tuple[float, float, float, float]) -> str:
    """Build search data for request.
    
    Parameters
    ----------
     amenities: list[str]
     bound : tuple
     
    Return
    ------
     data as text: str

    """
    amenity_string = "|".join(amenities)
    data = f"""
        [out:json];
        node
          ["amenity"~"{amenity_string}"]
          {bound};
        out;
    """
    return data


@click.command()
@click.option("--amenities", '-a', type=click.STRING, help="Type of amenity, i.e. cafe", multiple=True, default=[])
@click.argument("output_feature_file", type=click.Path(writable=True))
def cli(amenities: list[str], output_feature_file: str) -> None:
    """Download amenity features.
    
    Parameters
    ----------
     amenities: list[str]
     output_feature_file: str
     
    Return
    ------
     nothing
     
    """
    res = requests.post(OVERPASS_URL, data=get_search_data(amenities, AREA_BOUND))
    res_data = json.loads(res.content)
    with open(output_feature_file, 'w', encoding='utf-8') as f:
        json.dump(res_data[ITEMS_KEY], f)
        

if __name__ == "__main__":
    cli()