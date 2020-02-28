import pandas as pd
import pathlib


def write_csv(dataSet, location):
    success = True
    if isinstance(location, pathlib.Path):
        location = location.name
    else:
        location = location
    try:
        dataSet.to_csv(location + ".csv", index=False)
        return success
    except AttributeError:
        success = False
        return success


if __name__ == "__main__":
    write_csv()
