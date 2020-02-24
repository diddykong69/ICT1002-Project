import pandas as pd


def write_csv(dataSet, location):
    success = True
    try:
        dataSet.to_csv(location + ".csv", index=False)
        return success
    except AttributeError:
        success = False
        return success


if __name__ == "__main__":
    write_csv()
