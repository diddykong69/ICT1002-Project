"""
Author      : How Shun Han
Description : The writer modules takes in the data frame that has been processed by other modules and functions and
            transform the data frame into an csv file when the user chooses to export the data.
"""

import pathlib


def write_csv(dataSet, location):
    success = True
    try:
        if isinstance(location, pathlib.Path):
            location = str(location.resolve())
            dataSet.to_csv(location + ".csv", index=False)
            return success
        else:
            location = location
            dataSet.to_csv(location + ".csv", index=False)
            return success
    except AttributeError:
        success = False
        return success


if __name__ == "__main__":
    write_csv()
