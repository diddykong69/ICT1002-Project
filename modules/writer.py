import pandas as pd


def write_csv(data_set, location):
    success = True
    try:
        data_set.to_csv(location + ".csv", index=False)
        return success
    except AttributeError:
        success = False
        return success


if __name__ == "__main__":
    write_csv()
