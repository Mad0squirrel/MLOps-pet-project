"""Script for cleaning data."""

import re
from typing import Union

import click
import numpy as np
import pandas as pd

ELEVATOR_FEATURE = 'elevator'
FLOORS_FEATURE = 'number of floors'
APARTMENT_FLOOR_FEATURE = 'apartment floor'
ADDRESS_FEATURE = 'physical address'
BATHROOM_FEATURE = 'bathroom'
AREA_FEATURE = 'area of apartment'
HOUSE_TYPE_FEATURE = 'type of house'
ROOMS_FEATURE = 'number of rooms'
TARGET = 'price'
NON_NULL_FEATURES = [
    ADDRESS_FEATURE,
    FLOORS_FEATURE,
    HOUSE_TYPE_FEATURE,
    ROOMS_FEATURE,
    AREA_FEATURE,
    APARTMENT_FLOOR_FEATURE,
    TARGET,
]
REPAIR_FEATURE = 'repair'
TERRACE_FEATURE = 'terrace'
NULL_FEATURES = [REPAIR_FEATURE, TERRACE_FEATURE]
ALL_FEATURES = NON_NULL_FEATURES + NULL_FEATURES + [ELEVATOR_FEATURE, BATHROOM_FEATURE]


def extract_first_int(number: Union[str, int]) -> int:
    """Extract first int from string or return int if passed int.
    
    Parameters
    ----------
     number : Union[str, int]
    
    Returns
    -------
     first number: int

    """
    if isinstance(number, int):
        return number
    numbers = re.findall(r"\d+", number)
    if not numbers:
        raise ValueError(f" '{number}' doesnt contain any integer number")
    return int(numbers[0])

def get_min_elevator_count_by_floor_count(floor_count: int) -> int:
    """Calculate min elevator count on info about floor.
    
    Parameters
    ----------
     floor_count: int
    
    Returns
    -------
     elevator count: int
     
    """
    if isinstance(floor_count, str):
        raise ValueError(floor_count)
    if floor_count <= 5:
        return 0
    elif 6 <= floor_count <= 9:
        return 1
    elif 10 <= floor_count <=19:
        return 2
    else:
        return 3
    
def get_street_and_house_from_address(address: str) -> str:
    """Get street and house from address.
    
    Parameters
    ----------
     address: str
    
    Returns
    -------
     street: str, house number: str
     
    """
    street_part_map = {
        "ул.": "улица",
        "улица": "улица",
        "пр-т": "проспект",
        "пр.": "проезд",
        "ш.": "шоссе",
        "б-р": "бульвар",
        "пер.": "переулок",
        "проезд": "проезд",
        "наб.": "набережная",
        "пр-д": "проезд",
        "дер.": "деревня",
        "туп.": "тупик",
        "аллея": "аллея",
        "жилой комплекс": "жилой комплекс",
        "квартал": "квартал",
    }
    address_parts = address.split(", ")
    street = ""
    house = ""
    building = ""
    ownership = ""
    only_number = ""
    
    for part in address_parts:
        for old_part, new_part in street_part_map.items():
            if old_part in part:
                street = part.replace(old_part, new_part).strip()
                break
        if "д." in part:
            house = part.replace("д.", "").strip()
        elif "стр." in part:
            building = part.replace("стр.", "").strip()
        elif "вл." in part:
            ownership = part.replace("вл.", "").strip()
        else:
            only_number = address.split(", ")[-1]
    
    if street and house:
        return f"{street}, {house}"
    elif street and building:
        return f"{street}, {building}"
    elif street and ownership:
        return f"{street}, {ownership}"
    elif street and only_number:
        return f"{street}, {only_number}"
    else:
        return "Улица и номер дома не найдены"

def get_room_count_by_name(room_name: str) -> int:
    """Get count of rooms by specific name.
    
    Parameters
    ----------
     room_name: str
     
    Returns
    -------
     count of rooms: int
    
    """
    if room_name.isdigit():
        return int(room_name)
    if room_name in ("студия", "свободная планировка"):
        return 1
    raise ValueError(f"Unknown room type: {room_name}, {type(room_name)}")


@click.command()
@click.argument("input_feature_file", type=click.Path(readable=True))
@click.argument("output_feature_file", type=click.Path(writable=True))
def cli(input_feature_file: str, output_feature_file: str) -> None:
    """Clean data.
    
    Parameters
    ----------
     input_feature_file: input filepath
     output_feature_file: output filepath
    
    Returns
    -------
     nothing
    
    """
    df = pd.read_csv(input_feature_file)
    
    for feature in NON_NULL_FEATURES:
        df = df[df[feature].notna()]
    # address
    df[ADDRESS_FEATURE] = df[ADDRESS_FEATURE].apply(get_street_and_house_from_address)
    # bathroom
    df[BATHROOM_FEATURE] = df[BATHROOM_FEATURE].fillna("неизвестно")
    df = df[df[BATHROOM_FEATURE].apply(lambda x: len(x) < 30)] # filter anomaly values
    # type of house
    df = df[df[HOUSE_TYPE_FEATURE].apply(lambda x: len(x) < 20)] # filter anomaly values
    # area
    df[AREA_FEATURE] = df[AREA_FEATURE].apply(lambda x: float(x[:-3])).astype(np.float64)
    # room count
    df = df[df[ROOMS_FEATURE] != "многокомнатная"]
    df[ROOMS_FEATURE] = df[ROOMS_FEATURE].apply(get_room_count_by_name)
    #floor count
    df[FLOORS_FEATURE] = df[FLOORS_FEATURE].apply(extract_first_int).astype(np.int64)
    df[APARTMENT_FLOOR_FEATURE] = df[APARTMENT_FLOOR_FEATURE].astype(np.int64)
    # features where we allow non-null values
    for feature in NULL_FEATURES:
        df[feature] = df[feature].fillna("нет")
    # repair
    df = df[df[REPAIR_FEATURE].apply(lambda x: len(x) < 20)]  # filter anomaly values
    # elevator
    min_elevator_counts = df[FLOORS_FEATURE].apply(get_min_elevator_count_by_floor_count).values
    df[ELEVATOR_FEATURE] = np.where(df[ELEVATOR_FEATURE].isna(), min_elevator_counts, df[ELEVATOR_FEATURE].values)
    df[ELEVATOR_FEATURE] = df[ELEVATOR_FEATURE].replace({'нет': 0}).astype(np.int64)
    # save
    df[ALL_FEATURES].to_csv(output_feature_file, index=False)
    # logging
    click.echo(df[ALL_FEATURES].info())


if __name__ == "__main__":
    cli()
        