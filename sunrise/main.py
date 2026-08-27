from dataclasses import dataclass
import datetime as dt
from pathlib import Path

import numpy as np


@dataclass
class SunriseDay:
    day: int
    sunrise_time: dt.date
    sunset_time: dt.date


@dataclass
class SunriseMonth:
    month: int
    sunrise_days: list[SunriseDay]


@dataclass
class SunriseYear:
    year: int
    months: list[SunriseMonth]


def load_sunrise_data(file_path):

    location: str = ""
    zone: str = ""
    data_block_start = -1  # placeholder for the line number where the data block starts

    with open(file_path, "r") as file:
        data = file.readlines()
        data = [line.strip().lower() for line in data if line.strip() and not line.startswith("#")]

    for i, line in enumerate(data):
        if line.startswith("location:"):
            location = line.split(":")[1].strip()

        if line.startswith("zone:"):
            zone = line.split(":")[1].strip()

        if line.startswith("jan."):
            data_block_start = i

    while True:
        try:
            data_block = data[data_block_start:]
            data_block = [line.split() for line in data_block]
            data_block = np.array(data_block)
            break
        except Exception as e:
            print(f"Error processing data block: {e}")
            data_block_start += 1
            if data_block_start >= len(data):
                raise ValueError("Could not find a valid data block in the file.")

    return data


def main():
    parent_dir = Path(__file__).parent
    data_file = parent_dir / "raw_data" / "2026_data.txt"
    print(f"Loading sunrise data from: {data_file}")
    sunrise_data = load_sunrise_data(data_file)


if __name__ == "__main__":
    main()
